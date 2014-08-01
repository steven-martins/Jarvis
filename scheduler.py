__author__ = 'Steven'

from threading import Thread
from storage import Storage
import time, json, parsedatetime

from message import Notif

class Scheduler(Storage, Thread):
    def __init__(self, bot):
        Thread.__init__(self, name="Scheduler")
        self._bot = bot

    def run(self):
        while True:
            try:
                while len(self.getDb().zrangebyscore("notif", 0, time.time())) > 0:
                    print("Something to do")
                    arr = self.getDb().zrange("notif", 0, 0, withscores=True)
                    print("[Scheduler] %s" % str(arr))
                    if len(arr) > 0 and int(arr[0][1]) < time.time():
                        obj = arr[0][0]
                        self.getDb().zrem("notif", obj)
                        n = Notif(obj)
                        print("Notif: %s" % str(n))
                        self._bot.event("notif", obj)
                        print("[Scheduler] consumed: %s" % str(obj))
                time.sleep(1)
            except Exception as e:
                print(str(e))
                time.sleep(1)
                break
            except:
                time.sleep(5)


if __name__ == "__main__":
    #s = Storage()
    #s.getDb().zadd("notif", json.dumps({"room": "skies",
    #                                                 "message": "Ceci est un test",
    #                                                 "type": "notification"}), float(time.time()))
    pass