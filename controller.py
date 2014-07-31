__author__ = 'Steven'

import shlex
import types
import os, inspect, re, imp, sys
import pyclbr
from actions.Action import Action
from actions.base import Ask
from actions.fun import Coffee, ImageMe

PLUGINS = [
    "actions",
    ]

HANDLE = "Jarvis"

class Controller():
    def __init__(self):
        self._actions = {}

        self.plugins = []
        self.plugins_dirs = {}

        self.discover()
        self.autoregister()

        #self.registerAction("^@%s help" % HANDLE, self.help)
        #self.registerAction("^@%s ask" % HANDLE, Ask)


    def discover(self):
        for plugin in PLUGINS:
            path_name = None
            for mod in plugin.split('.'):
                if path_name is not None:
                    path_name=[path_name]
                file_name, path_name, description = imp.find_module(mod, path_name)
            self.plugins_dirs[os.path.abspath(path_name)] = plugin
        self.plugins_dirs = dict(zip(self.plugins_dirs.values(),self.plugins_dirs.keys()))

        plugin_modules = {}

        for plugin_name, plugin_root in self.plugins_dirs.items():
            for root, dirs, files in os.walk(plugin_root, topdown=False):
                for f in files:
                    if f[-3:] == ".py" and f != "__init__.py":
                        try:
                            module_path = os.path.join(root, f)
                            path_components = os.path.split(module_path)
                            module_name = path_components[-1][:-3]
                            full_module_name = ".".join(path_components)
                            # Need to pass along module name, path all the way through
                            combined_name = ".".join([plugin_name, module_name])

                            module = imp.load_source(module_name, module_path)
                            for class_name, cls in inspect.getmembers(module, predicate=inspect.isclass):
                                try:
                                    if hasattr(cls, "is_action") and class_name != "Action":
                                        self.plugins.append({
                                            "name": class_name,
                                            "class": cls,
                                            "module": module,
                                            "full_module_name": full_module_name,
                                            })
                                except Exception as e:
                                    print("Error bootstrapping %s: %s" % (class_name, str(e)))
                        except Exception as e:
                            print("Error loading %s: %s" % (module_path, str(e)))

    def autoregister(self):
        for plugin_info in self.plugins:
            for function_name, fn in inspect.getmembers(plugin_info["class"], predicate=inspect.ismethod):
                if hasattr(fn, "meta") and "regex" in fn.meta:
                    regex = fn.meta["regex"]
                    regex = "(?i)%s" % regex
                    if fn.meta["only_to_direct_mentions"]:
						regex = "@%s %s" % (HANDLE, regex)
                    self.registerAction(regex, {
                        "function_name": function_name,
                        "class_name": plugin_info["name"],
                        "fn": getattr(plugin_info["class"](), function_name),
                        "regex_pattern": fn.meta["regex"],
                        "direct_mentions_only": fn.meta["only_to_direct_mentions"],
                        "private_only": fn.meta["private_only"],
                        "admin_only": fn.meta["only_to_admin"],
                        "__doc__": fn.meta["__doc__"]
                    })
        print(str(self._actions))
        #sys.exit(1)





    def help(self, *args, **kwargs):
        print("args: " + str(args))
        print("kwargs: " + str(kwargs))
        """ Display this message."""
        msg = "For you, I'm able to do:\n"
        for k, v in self._actions.items():
            if isinstance(v, types.DictType):
                msg += " o " + k + ": " + str(v["__doc__"]) + "\n"
            else:
                msg += " o " + k + ": " + str(v.__doc__) + "\n"
        return msg

    def registerAction(self, word, cmd):
        self._actions[word] = cmd

    def unregisterAction(self, word):
        if word in self._actions:
            del self._actions[word]

    def _do(self, action, params, mtype, mfrom):
        print("action: " + action)
        print("params: " + str(params))
        for k, v in self._actions.items():
            #if action in self._actions:
            print("re.search('%s', '%s')" % (k, " ".join([action] + params)))
            match = re.search(k, " ".join([action] + params))
            if match and ((mtype == "groupchat" and v["private_only"] == False)
                            or (mtype != "groupchat" and v["private_only"] == True)):
                print("matched: %s" % k)
                dict = match.groupdict()
                dict["mfrom"] = mfrom
                #if isinstance(v, types.FunctionType):
                #    return v(params, **dict)
                #elif isinstance(v, types.DictType):
                return v["fn"](params, **dict)
                #elif isinstance(v, types.MethodType):
                #    return v(self, params, **dict)
                #elif issubclass(v, Action):
                #    return v().run(params, **dict)
                #raise Exception("Unknown action")
        if mtype == "chat":
            raise Exception("Unknown action")
        return None

    def do(self, msg, mtype="chat", mfrom=""):
        # acting as command line for now
        array = shlex.split(msg)
        if len(array) == 0:
            raise Exception("Wrong action")
        return self._do(array[0], array[1:], mtype, mfrom)
