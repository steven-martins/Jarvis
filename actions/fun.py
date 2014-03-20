__author__ = 'Steven'

from . import Action

class Coffee(Action.Action):
    """ Turn coffee into code"""
    def run(self, *args):
        return """I turn coffee into code, like you!
"""



class Tea(Action.Action):
    """ Give some tea at five o'clock only!"""
    def run(self, *args):
        return """It's to early! Try again around 5 o'clock.
"""
