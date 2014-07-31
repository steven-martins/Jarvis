__author__ = 'Steven'

import time
from actions import Action
from query import Question
from decorators import hear, respond_to

class ThanksPlugin(Action.Action):
    @respond_to("^(?:thanks|thank you|tx|thx|ty|tyvm)")
    def respond_to_thanks(self, *args, **kwargs):
        return "You're welcome!"

    @hear("(thanks|thank you|tx|thx|ty|tyvm),? (jarv|jarvis)")
    def hear_thanks(self, *args, **kwargs):
        return "You're welcome!"

class Hello(Action.Action):
    @respond_to("hi$")
    def hi(self, *args, **kwargs):
        """hi: I know how to say hello!"""
        return "hello!"

    @respond_to("hello$")
    def hello(self, *args, **kwargs):
        return "hi!"

class Love(Action.Action):
    @hear("i love(?: you,?)? (jarv|jarvis)")
    def hear_love(self, *args, **kwargs):
        return "I love you, too."

    @respond_to("i love you")
    def hear_love_direct(self, *args, **kwargs):
        return "I love you, too."

    @hear("(jarv|jarvis) is awesome")
    def hear_i_am_awesome(self, *args, **kwargs):
        return "Aww, thanks!"

    @respond_to("you(?: are|'re)? (?:awesome|rock)")
    def hear_you_are_awesome(self, params, mfrom, *args, **kwargs):
        return "Takes one to know one, %s." % mfrom

class Time(Action.Action):
    @respond_to("what time is it ?")
    def run(self, *args, **kwargs):
        return "Current time: %s" % (str(time.strftime("%H:%M:%S")))

class Date(Action.Action):
    @respond_to("what date is it ?")
    def run(self, *args, **kwargs):
        return "Current date: %s" % (str(time.strftime("%d/%m/%Y")))

class Ask(Action.Action):
    """Module for testing the questions system."""
    def run(self, *args, **kwargs):
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
