__author__ = 'Steven'

import re, json

class Msg(object):
    def __init__(self, msg):
        self.datas = {}
        self.body = msg["body"]
        self.mtype = msg["type"]
        self.mfrom = msg["from"]
        self.exp = msg["from"].bare
        self.mucnick = msg["mucnick"] if self.mtype == "groupchat" else None
        self.message = msg
        match = re.search("^[0-9]*_(?P<room>.*)@(\S| )+$", str(self.mfrom))
        self.room = match.group("room").replace("_", " ") if match and self.mtype == "groupchat" else None

    def __str__(self):
        return "body(%s), type(%s), from(%s), exp(%s), mucnick(%s), room(%s)" % (self.body, self.mtype, self.mfrom, self.exp, self.mucnick, self.room)


class Notif(dict):
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

    def __init__(self, j):
        try:
            datas = json.loads(j)
            for k, v in datas.items():
                self.__setattr__(k, v)
        except Exception as e:
            print("Notif loading exception: %s" % (str(e)))
        # check minimal:
        # room, message
        # bonus: date, type, content-type

