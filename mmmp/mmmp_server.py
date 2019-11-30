"""MagicMirror Management Protocol Server"""
import os
from flask import Flask, request
import json

CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config/config.js")
app = Flask(__name__)


def _ret_unknown_action(action):
    return "Unknown action '{}'".format(action), 500


def _ret_ok():
    return "OK", 200


def _ret_unknown_module(module):
    return "Found no matching modules for '{}'".format(module), 404


def _ret_unknown_param(param):
    return "Found no matching params for '{}'".format(param), 404


def _ret_invalid_request(missing_property):
    return "Invalid request, missing property '{}'".format(missing_property), 500


def write_config(config_json):
    """Write Python dict as JSON to format compatible with MagicMirror JS"""
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


@app.route('/top/', methods=['GET'])
def top_get():
    return read_config()


@app.route('/top/', methods=['POST'])
def top_set():
    write_config(request.json)
    return _ret_ok()


@app.route('/top/<string:param>/', methods=['GET'])
def top_param_get(param):
    config = read_config()
    ret = {"value": config[param]}
    return ret


@app.route('/top/<string:param>/', methods=['POST'])
def top_param_set(param):
    config = read_config()
    action = request.json["action"]

    if action == "update":
        if "value" not in request.json:
            return _ret_invalid_request("value")
        config[param] = request.json["value"]
    elif action == "delete":
        del config[param]
    else:
        return _ret_unknown_action(action)

    write_config(config)
    return _ret_ok()


@app.route('/modules/', methods=['GET'])
def module_list():
    config = read_config()
    ret = {"modules": [x["module"] for x in config["modules"]]}
    return ret


@app.route('/modules/', methods=['POST'])
def module_add():
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


@app.route('/modules/<string:module>/', methods=['GET'])
def module_get(module):
    config = read_config()
    module = [x for x in config["modules"] if x["module"] == module]

    if len(module) != 1:
        return _ret_unknown_module(module)

    ret = {"value": module[0]}
    return ret


@app.route('/modules/<string:module>/', methods=['POST'])
def module_set(module):
    config = read_config()

    action = request.json["action"]

    if action == "delete":
        modules = [x for x in config["modules"] if x["module"] != module]
        config["modules"] = modules
        write_config(config)
        return _ret_ok()
    else:
        return _ret_unknown_action(action)


@app.route('/modules/<string:modulename>/<string:param>/', methods=['GET'])
def module_get_param(modulename, param):
    config = read_config()
    module = [x for x in config["modules"] if x["module"] == modulename]

    if len(module) != 1:
        return _ret_unknown_module(modulename)
    if param not in module[0]:
        return _ret_unknown_param(param)

    ret = {"value": module[0][param]}
    return ret


@app.route('/modules/<string:modulename>/<string:param>/', methods=['POST'])
def module_set_param(modulename, param):
    config = read_config()
    module = [x for x in config["modules"] if x["module"] == modulename]

    if len(module) != 1:
        return _ret_unknown_module(modulename)
    if param not in module[0]:
        return _ret_unknown_param(param)

    action = request.json["action"]
    if action == "update":
        if "value" not in request.json:
            return _ret_invalid_request("value")
        module[0][param] = request.json["value"]
    elif action == "delete":
        del module[0][param]
    else:
        return _ret_unknown_action(action)

    write_config(config)
    return _ret_ok()


if __name__ == "__main__":
    app.run(debug=True)
