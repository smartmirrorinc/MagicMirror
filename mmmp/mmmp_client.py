#!/usr/bin/env python3
import npyscreen
import requests
import json
import sys


HOST = "127.0.0.1"
PORT = "5000"
URL = "http://{}:{}/".format(HOST, PORT)


class Get404Exception(Exception):
    pass


def do_get(path):
    r = requests.get('{}{}'.format(URL, path))
    if r.status_code != 200:
        if r.status_code == 404:
            raise Get404Exception()
        else:
            raise NotImplementedError("Request failed")
    try:
        return r.json()
    except:
        return str(r.content)


def do_post_json(path, data):
    r = requests.post("{}{}".format(URL, path), json=data)

    if r.status_code != 200:
        raise NotImplementedError("post fail")


class App(npyscreen.StandardApp):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.editmoduleform = self.addForm("MAIN", EditModuleForm, name="Module configurator")
        self.addmoduleform = self.addForm("ADDMODULE", AddModuleForm, name="Add custom module")
        self.addinstalledform = self.addForm("ADDINSTALLED", AddInstalledForm, name="Add installed module",
                                             lines=25)
        import curses
        curses.mousemask(0)

class EditModuleForm(npyscreen.ActionFormV2WithMenus):
    def create(self):
        self.text = self.add(npyscreen.FixedText, value="")
        self.modules = self.add(npyscreen.MultiLine, values=[], width=20)
        self.modules.value_changed_callback = self.populate_and_goto_editfield
        self.nextrely = 3
        self.nextrelx = 30
        self.editfield = self.add(npyscreen.MultiLineEdit, name="edittxt", value="", title="asdf")
        self.populate()
        self.lastmodule = None

        self.nav_menu = self.new_menu(name="Module")
        self.nav_menu.addItem(text="Add custom", onSelect=self.menu_add_custom)
        self.nav_menu.addItem(text="Add installed", onSelect=self.menu_add_installed)
        self.nav_menu.addItem(text="Delete selected", onSelect=self.menu_delete)

        self.manage_menu = self.nav_menu.addNewSubmenu(name="Management")
        self.manage_menu.addItem(text="Restart", onSelect=self.menu_manage_restart)
        self.manage_menu.addItem(text="Stop", onSelect=self.menu_manage_stop)
        self.manage_menu.addItem(text="Start", onSelect=self.menu_manage_start)
        self.manage_menu.addItem(text="HDMI ON", onSelect=self.menu_manage_hdmi_on)

        self.nav_menu.addItem(text="Quit", onSelect=self.quit)

        self.add_handlers({"h": self.show_helptxt})

    def show_helptxt(self, key):
        if self.modules.value is not None and self.modules.value < len(self.modules.values):
            module = self.modules.values[self.modules.value]
            curr = do_get("config/modules/{}/".format(module))["value"]
            if "_meta" in curr and "help-url" in curr["_meta"]:
                npyscreen.notify_confirm(curr["_meta"]["help-url"], title='Help')
                return
        npyscreen.notify_confirm("No help available", title='Help')

    def quit(self):
        sys.exit()

    def on_cancel(self):
        self.quit()

    def menu_add_custom(self):
        self.parentApp.addmoduleform.edit()

    def menu_add_installed(self):
        self.parentApp.addinstalledform.populate()
        self.parentApp.addinstalledform.edit()

    def menu_delete(self):
        if self.modules.value is None or self.modules.value >= len(self.modules.values):
            npyscreen.notify_confirm("No module selected", title='Error')
        else:
            module = self.modules.values[self.modules.value]
            prompt = npyscreen.notify_yes_no("Delete module {}?".format(module), title='Prompt')
            if prompt:
                do_post_json("config/modules/{}/".format(module),
                             {"action": "delete"})
                self.populate()

    def menu_manage_restart(self):
        do_get("/manage/restart/")
        npyscreen.notify_confirm("MagicMirror restarting", title='Success')

    def menu_manage_stop(self):
        do_get("/manage/stop/")
        npyscreen.notify_confirm("MagicMirror stopping", title='Success')

    def menu_manage_start(self):
        do_get("/manage/start/")
        npyscreen.notify_confirm("MagicMirror starting", title='Success')

    def menu_manage_hdmi_on(self):
        do_get("/manage/hdmi_on/")
        npyscreen.notify_confirm("HDMI turning ON", title='Success')

    def populate(self):
        self.modules.values = do_get("config/modules/")["modules"]

    def populate_and_goto_editfield(self, widget):
        if self.modules.value is None or self.modules.value >= len(self.modules.values):
            self.editfield.value = ""
        else:
            module = self.modules.values[self.modules.value]
            if module != self.lastmodule:
                curr = do_get("config/modules/{}/".format(module))["value"]
                if "_meta" in curr:
                    self.current_module_meta = curr["_meta"]
                    del curr["_meta"]
                else:
                    self.current_module_meta = None
                self.editfield.value = json.dumps(curr, indent=2)
                self.lastmodule = module
                self.modules.display()
                self.editfield.edit()

    def on_ok(self):
        if self.modules.value is not None:
            edittxt = self.editfield.value
            module = self.modules.values[self.modules.value]

            try:
                edittxt_dict = json.loads(edittxt)
                if self.current_module_meta is not None:
                    edittxt_dict["_meta"] = self.current_module_meta
                do_post_json("config/modules/{}/".format(module), 
                             {"action": "update", "value": edittxt_dict})
                self.populate()
                npyscreen.notify_confirm("Changes saved", title='Success')
            except json.decoder.JSONDecodeError as ex:
                npyscreen.notify_confirm("JSON decode error at line {}, col {}:\n{}"\
                                         .format(ex.lineno, ex.colno, ex.msg),
                                         title='Error')


class AddModuleForm(npyscreen.ActionPopup):
    def create(self):
        self.helptxt = self.add(npyscreen.FixedText, value="Module name:")
        self.module = self.add(npyscreen.Textfield, value="")

    def on_ok(self):
        if self.module.value is not None and len(self.module.value) > 0:
            added_modules = do_get("config/modules/")["modules"]
            module_to_add = self.module.value
            if module_to_add in added_modules:
                npyscreen.notify_confirm("Cannot add module {} twice".format(module_to_add), 
                                         title='Error')
            else:
                d = {"module": module_to_add}
                do_post_json("config/modules/", 
                             {"action": "add", "value": d})
                self.parentApp.editmoduleform.populate()


class AddInstalledForm(npyscreen.ActionPopup):
    def create(self):
        self.helptxt = self.add(npyscreen.FixedText, value="Module to add:")
        self.modules = self.add(npyscreen.MultiLine, values=[])

    def populate(self):
        added_modules = do_get("config/modules/")["modules"]
        installed_modules = do_get("manage/listmodules/")["value"]
        self.modules.values = [x for x in installed_modules if x not in added_modules]

    def on_ok(self):
        if self.modules.value is not None and self.modules.value < len(self.modules.values):
            added_modules = do_get("config/modules/")["modules"]
            module_to_add = self.modules.values[self.modules.value]
            if module_to_add in added_modules:
                npyscreen.notify_confirm("Cannot add module {} twice".format(module_to_add), 
                                         title='Error')
            else:
                try:
                    d = do_get("template/modules/{}".format(module_to_add))["value"]
                except Get404Exception:
                    d = {"module": module_to_add}

                do_post_json("config/modules/", 
                             {"action": "add", "value": d})
                self.parentApp.editmoduleform.populate()


MyApp = App()
MyApp.run()

