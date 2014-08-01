__author__ = 'Steven'

from storage import Storage
from hipchat import HipChat

from message import Msg

class Action(Storage, HipChat):
    is_action = True

    def __init__(self):
        self._version = 1.0

    def run(self, *args):
        pass
