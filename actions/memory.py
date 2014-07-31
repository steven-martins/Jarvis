__author__ = 'Steven'

from decorators import hear, respond_to, one_to_one
from actions import Action

class Memory(Action.Action):

    @one_to_one("^How big is the db?", admin_only=True)
    def db_size(self, *args, **kwargs):
        return "Currently, %s of memory are used." % self.getStorageInfos()["used_memory_human"]

    @one_to_one("^Clear (?P<key>.*)", admin_only=True)
    def clear_storage(self, params, key, *args, **kwargs):
        if not key:
            return "Sorry, you didn't say what to clear."
        else:
            self.clear(key)
            return "Ok. Clearing the storage for %s" % key

    @one_to_one("^Show (?:me )?(?:the )?storage for (?P<key>.*)", admin_only=True)
    def show_storage(self, params, key=None, *args, **kwargs):
        if not key:
            return "Not sure what you're looking for."
        else:
            val = self.load(key)
            return "%s is %s" % (key, val)

    @one_to_one("^Store (?:me )?(?P<value>.*) for (?P<key>.*)", admin_only=True)
    def add_storage(self, params, key=None, value=None, *args, **kwargs):
        if not key:
            return "Not sure what you're looking for."
        else:
            val = self.store(key, value)
            return "Okay, done." if val else "Something goes wrong: value(%s), key(%s)" % (value, key)
