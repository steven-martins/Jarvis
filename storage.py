__author__ = 'Steven'

import redis, datetime

from message import Notif

class Storage(object):
    _db = None

    def getDb(self):
        if not Storage._db:
            Storage._db = redis.Redis('localhost', db=0) #temp
        return Storage._db

    def getStorageInfos(self):
        return self.getDb().info()

    def clear(self, key):
        return self.getDb().delete(key)

    def load(self, key):
        return self.getDb().get(key)

    def store(self, key, value, type="key"):
        if type == "key":
            return self.getDb().set(key, value)
        return False

    def addNotif(self, timestamp, notif):
        self.getDb().zadd("notif", notif.toJson(), float(timestamp))

    def notifs(self, type="reminder", owner=None):
        elems = self.getDb().zrange("notif", 0, -1, withscores=True)
        res = []
        for a in elems:
            d_str = datetime.datetime.fromtimestamp(int(a[1])).strftime('%Y-%m-%d %H:%M')
            n = Notif(a[0])
            print("n: " + str(n))
            if not owner or (hasattr(n, "owner") and n.owner == owner):
               res.append((d_str, n))
        return res
