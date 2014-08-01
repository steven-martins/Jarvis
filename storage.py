__author__ = 'Steven'

import redis

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