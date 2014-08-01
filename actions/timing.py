__author__ = 'Steven'

from actions import Action
from decorators import hear, respond_to

import time, json, parsedatetime, datetime

from message import Notif

class Timing(Action.Action):

    @respond_to("remind (?P<to>.*) in (?P<da>.*) to (?P<action>.*)$")
    def remind_me(self, message, to, da, action):
        cal = parsedatetime.Calendar()
        d = time.mktime(cal.parse(da)[0])
        obj_d = datetime.datetime.fromtimestamp(d)
        print("timing(%s), action(%s)" % (str(obj_d.strftime("%Y-%m-%d %H:%M:%S")), action))
        notif = Notif()
        notif.room = message.room
        notif.message = action
        notif.type = "reminder"
        notif.timestamp = d
        notif.date = str(obj_d.strftime("%Y-%m-%d %H:%M:%S"))
        notif.inserted_at = int(time.time())
        notif.to = message.mucnick if to == "me" else ("Jarvis" if to == "you" else to)
        notif.owner = message.mucnick
        print(str(notif))
        self.addNotif(d, notif)
        return "Ok it's noted, %s" % message.mucnick

    @respond_to("display my reminder(s)?")
    def display_reminder(self, message):
        elems = self.notifs(type="reminder", owner=message.mucnick)
        s = "Your reminder: \n"
        for e in elems:
            s += " %s : %s\n" % (str(e[0]), e[1].message)
        return s
