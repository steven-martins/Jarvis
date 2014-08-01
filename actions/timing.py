__author__ = 'Steven'

from actions import Action
from decorators import hear, respond_to

import time, json, parsedatetime, datetime

from message import Notif

class Timing(Action.Action):

    @respond_to("remind me in (?P<date>.*) to (?P<action>.*)$")
    def remind_me(self, message, date, action):
        cal = parsedatetime.Calendar()
        d = time.mktime(cal.parse(date)[0])
        obj_d = datetime.datetime.fromtimestamp(d)
        print("timing(%s), action(%s)" % (str(obj_d.strftime("%Y-%m-%d %H:%M:%S")), action))
        notif = Notif()
        notif.room = message.room
        notif.message = action
        notif.type = "remind"
        notif.to = message.mucnick
        print(str(notif))
        self.addNotif(d, notif)
        return "Ok it's noted, %s" % message.mucnick