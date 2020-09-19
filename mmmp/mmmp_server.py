"""MagicMirror Management Protocol Server"""
import os
import subprocess
import glob
import json
from flask import Flask, request, jsonify


CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config/config.js")
app = Flask(__name__)


def _ret_unknown_action(action):
    return "Unknown action '{}'".format(action), 500


def _ret_ok():
    return "OK", 200


def _ret_unknown_template(template):
    return "Found no matching templates for '{}'".format(template), 404


def _ret_unknown_module(module):
    return "Found no matching modules for '{}'".format(module), 404


def _ret_unknown_param(param):
    return ("Found no matching params for '{}'".format(param), 404)


def _ret_invalid_request(missing_property):
    return "Invalid request, missing property '{}'".format(missing_property), 500


def _traverse_module(module, path):
    end_node = module
    for i in range(len(path)):  # pylint: disable=consider-using-enumerate
        if path[i] not in end_node:
            return False, _ret_unknown_param("/".join(path[:i+1]))
        end_node = end_node[path[i]]

    return True, end_node


def _sort_modules(module_list):
    return sorted(
        module_list,
        key=lambda x: x["_meta"]["order"] if "_meta" in x and "order" in x["_meta"] else 100000)


def write_config(config_json):
    """Write Python dict as JSON to format compatible with MagicMirror JS"""
    config_json["modules"] = _sort_modules(config_json["modules"])
    with open(CONFIG_FILE_PATH, "w") as f:
        f.write("/* Auto-generated file, do not edit */\n")
        f.write("var config = ")
        f.write(json.dumps(config_json, indent=4))
        f.write(";\n\n")
        f.write("/*************** DO NOT EDIT THE LINE BELOW ***************/\n")
        f.write("if (typeof module !== \"undefined\") {module.exports = config;}\n")


def read_config():
    """Read config.js to format parsable with json.loads()"""
    config_json = "{"
    with open(CONFIG_FILE_PATH, "r") as f:
        # Skip until we find "var config = {" line
        line = f.readline()
        while not line.startswith("var config = {"):
            line = f.readline()
            continue

        line = f.readline()
        while not line.startswith("};"):
            config_json += line
            line = f.readline()

        config_json += "}"

    return json.loads(config_json)


@app.route('/manage/<string:action>/', methods=['GET'])
def manage_action(action):
    """Management actions

    Handle management actions that are not directly related to a specific
    module, but manage the MagicMirror service. Actions such as
    start/stop/restart, turning the monitor on and off etc. belong here.
    """
    if action == "listmodules":  # list available modules
        thisdir = os.path.dirname(os.path.abspath(__file__))

        # default modules are represented by directories in modules/default/
        default_modules = os.path.abspath(os.path.join(thisdir, "../modules/default/*"))
        default_modules = [x for x in glob.glob(default_modules) if os.path.isdir(x)]

        # custom modules are represented by directories in modules/ (except "default")
        custom_modules = os.path.abspath(os.path.join(thisdir, "../modules/*"))
        custom_modules = [x for x in glob.glob(custom_modules) if os.path.isdir(x)
                          and os.path.basename(x) != "default"]

        # build list of all module names
        all_modules = default_modules + custom_modules
        all_modules = [os.path.basename(x) for x in all_modules]

        return jsonify({"value": all_modules})

    if action == "hdmi_on":  # force monitor ON
        thisdir = os.path.dirname(os.path.abspath(__file__))
        hdmi_on_script = os.path.abspath(os.path.join(
            thisdir, "../modules/MMM-PIR-Sensor/hdmi-on.sh"))
        subprocess.call("/bin/bash {}".format(hdmi_on_script).split(" "))
        return _ret_ok()

    if action in ["start", "stop", "restart"]:  # start/stop/restart MagicMirror² service
        subprocess.call("pm2 {} mm".format(action).split(" "))
        return _ret_ok()

    return _ret_unknown_action(action)


@app.route('/config/top/', methods=['GET'])
def config_top_get():
    """Get the entire config file"""
    return jsonify(read_config())


@app.route('/config/top/', methods=['POST'])
def config_top_set():
    """Set the entire config file"""
    write_config(request.json)
    return _ret_ok()


@app.route('/config/top/<path:path>/', methods=['GET'])
def config_top_path_get(path):
    """Get entry in config top-level

    For anything not in the modules section.
    """
    config = read_config()

    path = path.split("/")
    success, end_node = _traverse_module(config, path)
    if not success:
        return end_node

    ret = {"value": end_node}
    return jsonify(ret)


@app.route('/config/top/<path:path>/', methods=['POST'])
def config_top_path_set(path):
    """Set entry in config top-level

    For anything not in the modules section.
    """
    config = read_config()
    action = request.json["action"]

    path = path.split("/")
    success, end_node = _traverse_module(config, path[:-1])
    if not success:
        return end_node

    if action == "update":
        if "value" not in request.json:
            return _ret_invalid_request("value")
        end_node[path[-1]] = request.json["value"]
    elif action == "delete":
        del end_node[path[-1]]
    else:
        return _ret_unknown_action(action)

    write_config(config)
    return _ret_ok()


@app.route('/config/modules/', methods=['GET'])
def config_module_list():
    """List configured modules

    For available modules, refer to manage/listmodules
    """
    config = read_config()
    ret = {"modules": [x["module"] for x in config["modules"]]}
    return jsonify(ret)


@app.route('/config/modules/', methods=['POST'])
def config_module_add():
    """Add module for configuration

    Add an available module to the config file
    """
    config = read_config()
    action = request.json["action"]

    if action == "add":
        if "value" not in request.json:
            return _ret_invalid_request("value")
        config["modules"].append(request.json["value"])
        write_config(config)
        return _ret_ok()
    else:
        return _ret_unknown_action(action)


@app.route('/template/modules/<string:module>/', methods=['GET'])
def template_module_get(module):
    """Get template configuration for a module"""
    tmplfile = "templates/{}.json".format(module)

    if os.path.isfile(tmplfile):
        with open(tmplfile, "r") as f:
            tmpl = json.loads(f.read())
            return jsonify({"value": tmpl})

    return _ret_unknown_template(module)


@app.route('/config/modules/<string:module>/', methods=['GET'])
def config_module_get(module):
    """Get current configuration of an entire module"""
    config = read_config()
    module = [x for x in config["modules"] if x["module"] == module]

    if len(module) != 1:
        return _ret_unknown_module(module)

    ret = {"value": module[0]}
    return jsonify(ret)


@app.route('/config/modules/<string:module>/', methods=['POST'])
def config_module_set(module):
    """Change or delete configuration of an entire module"""
    config = read_config()

    action = request.json["action"]

    if action == "delete":
        modules = [x for x in config["modules"] if x["module"] != module]
        config["modules"] = modules
        write_config(config)
        return _ret_ok()
    elif action == "update":
        modules = [x for x in config["modules"] if x["module"] != module]
        modules.append(request.json["value"])
        config["modules"] = modules
        write_config(config)
        return _ret_ok()
    else:
        return _ret_unknown_action(action)


@app.route('/config/modules/<string:modulename>/<path:path>/', methods=['GET'])
def config_module_get_path(modulename, path):
    """Get single parameter of a module"""
    config = read_config()
    module = [x for x in config["modules"] if x["module"] == modulename]

    if len(module) != 1:
        return _ret_unknown_module(modulename)

    path = path.split("/")

    success, end_node = _traverse_module(module[0], path)
    if not success:
        return end_node

    ret = {"value": end_node}
    return jsonify(ret)


@app.route('/config/modules/<string:modulename>/<path:path>/', methods=['POST'])
def config_module_set_path(modulename, path):
    """Set or delete single parameter of a module"""
    config = read_config()
    module = [x for x in config["modules"] if x["module"] == modulename]
    path = path.split("/")

    if len(module) != 1:
        return _ret_unknown_module(modulename)

    action = request.json["action"]
    if action == "update":
        if "value" not in request.json:
            return _ret_invalid_request("value")

        success, end_node = _traverse_module(module[0], path[:-1])
        if not success:
            return end_node

        end_node[path[-1]] = request.json["value"]

    elif action == "delete":
        success, end_node = _traverse_module(module[0], path[:-1])
        if not success:
            return end_node

        del end_node[path[-1]]

    else:
        return _ret_unknown_action(action)

    write_config(config)
    return _ret_ok()


if __name__ == "__main__":
    app.run(debug=True)
