__author__ = 'Steven'


from loader import Conf

import requests

class HipChat(object):
    def sayHtml(self, message, room=None, handle=None):
        if not handle:
            from controller import HANDLE
            handle = HANDLE
        if not room:
            raise Exception("Room not provided")
        data = {
            "room_id": room,
            "from": handle,
            "message_format": "html",
            "message": message,
        }
        conf = Conf("bot.conf").getSection("hipchat")
        r = requests.post("https://api.hipchat.com/v1/rooms/message?format=json&auth_token=%s" % conf["auth_token"], params=data)
        results = r.json()
        print(str(results))
        return results

    def sayImage(self, url, width="350px", room=None, handle=None):
        if room:
            self.sayHtml("<img width='%s' src='%s' />" % (width, url), room, handle)