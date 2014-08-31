__author__ = 'Steven'

from .client import ClientTask

class Zmq():
    def execute(self, message, name, args=[], header={}, identity=None):
        if not "room" in header:
            header["room"] = message.room
        if not "mucnick" in header:
            header["mucnick"] = message.mucnick
        print(header)
        self.exec_remote(name, args, header, identity)

    def exec_remote(self, name, args=[], header={}, identity=None):
        print("exec_remote %s(%s), hdr=%s" % (name, args, header))
        c = ClientTask.clients[identity] if identity and identity in ClientTask.clients else ClientTask.clients[0]
        c.send(name, args, header)
