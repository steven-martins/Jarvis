__author__ = 'Steven'

import re, json

class Msg(object):
    def __init__(self, msg, base=None):
        self.datas = {}
        self.base = base
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

"""
        notif = Notif()
        notif.room = message.room
        notif.message = action
        notif.type = "reminder"
        notif.timestamp = d
        notif.date = str(obj_d.strftime("%Y-%m-%d %H:%M:%S"))
        notif.inserted_at = int(time.time())
        notif.to = message.mucnick
        notif.owner = message.mucnick
"""
class Notif(dict):
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

    def __init__(self, j="{}"):
        try:
            if isinstance(j, dict):
                datas = j
            else:
                datas = json.loads(j)
            print("Loading a Notification: %s" % str(datas))
            for k, v in datas.items():
                self.__setattr__(k, v)
        except Exception as e:
            print("Notif loading exception: %s" % (str(e)))
        # check minimal:
        # room, message
        # owner
        # bonus: date, type, content-type

    @staticmethod
    def fromZero():
        return Notif()

    def toJson(self):
        return json.dumps(self)