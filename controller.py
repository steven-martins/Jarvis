__author__ = 'Steven'

import shlex
import types
import os, inspect, re
import pyclbr
from actions.Action import Action
from actions.base import Ask
from actions.fun import Coffee, ImageMe

class Controller():
    def __init__(self):
        self._actions = {}
        self.registerAction("help", self.help)
        self.registerAction("?", self.help)
        self.registerAction("ask", Ask)
        self.registerAction("list", self.list)
        self.registerAction("register", self.register)
        self.registerAction("unregister", self.unregister)
        self.registerAction("coffee", Coffee)
        self.registerAction('image me (?P<search_query>.*)$', ImageMe)
        self.registerAction("^reload actions!$", self.reload)

    def help(self, *args):
        """ Display this message."""
        msg = "For you, I'm able to do:\n"
        for act in self._actions:
            msg += " o " + act + ": " + str(self._actions[act].__doc__) + "\n"
        return msg

    def _list(self, package, super="Action.Action"):
        for mod in (os.path.splitext(elem)[0] for elem in os.listdir(package) if os.path.splitext(elem)[1] == ".py"):
            for name, value in pyclbr.readmodule("%s.%s" % (package, mod)).iteritems():
                    if super in value.super:
                        yield (value.module, name)

    def list(self, *args):
        """ List all plugins available """
        msg = "All plugins available:\n"
        for module, cl in self._list("actions"):
            msg += " o %s (%s.%s)\n" % (cl, module, cl)
        return msg

    def _import(self, name):
        components = name.split('.')
        print("components: " + str(components))
        mod = __import__('.'.join(components[:-1]), fromlist=[components[-1]])
        print(str(mod))
        try:
            return getattr(mod, components[-1])
        except Exception:
            reload(mod)
            return getattr(mod, components[-1])

    def unregister(self, *args):
        """ unregister action """
        self.unregisterAction(args[1])
        return "%s unregistered." % args[1]

    def reload(self, *args):
        pass

    def register(self, *args):
        """ register new actions: register name package.module.Class """
        print("register(" + str(args) + ")")
        if len(args) >= 2:
            try:
                inst = self._import(args[2])
                self.registerAction(args[1], inst)
                return "Action %s registered" % args[1]
            except Exception as e:
                return "Impossible to register this action: %s" % str(e)
        return "impossible to register this action. Some parameters are missing. try again."

    def registerAction(self, word, cmd):
        self._actions[word] = cmd

    def unregisterAction(self, word):
        if word in self._actions:
            del self._actions[word]

    def _do(self, action, params):
        print("action: " + action)
        print("params: " + str(params))
        for k, v in self._actions.items():
            #if action in self._actions:
            print("re.search('%s', '%s')" % (k, " ".join([action] + params)))
            match = re.search(k, " ".join([action] + params))
            if match:
                print("matched: %s" % k)
                dict = match.groupdict()
                if isinstance(v, types.FunctionType):
                    return v(params, **dict)
                elif isinstance(v, types.MethodType):
                    return v(self, params, **dict)
                elif issubclass(v, Action):
                    return v().run(params, **dict)
        raise Exception("Unknown action")

    def do(self, msg):
        # acting as command line for now
        array = shlex.split(msg)
        if len(array) == 0:
            raise Exception("Wrong action")
        return self._do(array[0].lower(), array[1:])