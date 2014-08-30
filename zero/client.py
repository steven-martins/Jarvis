__author__ = 'Steven'

import zmq
import sys
import threading
import uuid
import shlex

from .tools import Pack

# executer des actions zmq (synchrone?)
# recevoir des infos
    # Soit des notifs
    # Soit le resultat de l'action (avec id)

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, xmpp, identity=None):
        self.id = id
        threading.Thread.__init__ (self)
        self._context = None
        self._socket = None
        self._xmpp = xmpp
        self._identity = str(uuid.uuid4()) if not identity else identity


    def send(self, name, args=[], header={}):
        if not self._socket:
            raise Exception("Socket not available")
        self._socket.send(Pack.pack_cmd(name, args, header))


    def listen(self):
        poll = zmq.Poller()
        poll.register(self._socket, zmq.POLLIN)
        while True:
            sockets = dict(poll.poll(1000))
            if self._socket in sockets:
                msg = Pack.unpack_resp(self._socket.recv())
                print('Client %s received: %s' % (self._identity, msg))
                #self._xmpp.event('notif', Notif.fromZero(msg))

    def run(self, url='tcp://localhost:5570'):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.DEALER)
        self._socket.identity = self._identity.encode('ascii')
        self._socket.connect(url)
        print('Client %s started' % (self._identity))
        self.listen()
        self._socket.close()
        self._context.term()


