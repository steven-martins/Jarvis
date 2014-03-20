__author__ = 'Steven'

import time
from . import Action
from query import Question

class Time(Action.Action):
    def run(self, *args):
        return "Current time: %s" % (str(time.strftime("%H:%M:%S")))

class Date(Action.Action):
    def run(self, *args):
        return "Current date: %s" % (str(time.strftime("%d/%m/%Y")))

class Ask(Action.Action):
    """Module for testing the questions system."""
    def run(self, *args):
        return Question("How old are you ?", [
            ("-", lambda *args: "You're not born yet!"),
            ("42", lambda *args: "Oh, why 42 ?! U kiddin' ?"),
            ("^[0-9]+", lambda *args: "Ok, go with %s" % str(args)),
            ("^\W*", lambda *args: Question("You're weird. So what's your name ?", [
                ("Jarvis", lambda *args: "Oh, your name is like mine!! :)"),
                ("^\W*", lambda *args: "Hi %s" % str(args[0]))
            ]))
        ])
        #return Question("How are you ?", [
        #    ("fine", lambda *args: "Great!"),
        #    ("bad", lambda *args: "Oh, why ?!"),
        #    ("[a-zA-Z]*", lambda *args: "Hum %s" % str(args))
        #])
