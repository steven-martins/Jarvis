#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Steven'

import sys
import logging
import sleekxmpp
import ssl
import time
import types
from threading import Thread
from controller import Controller
from loader import Conf
from query import Question
from message import Msg

from hipchat import HipChat

from message import Notif

from scheduler import Scheduler
from zero.client import ClientTask

class Events(Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self._bot = bot

    def run(self):
        while 1:
            print("thread")
            obj = {}
            obj["type"] = "ping"
            obj["message"] = " "
            self._bot.event('my_ping', obj)
            time.sleep(60)


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')


class Jarvis(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, room):
        super(Jarvis, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('chatstate', self.chatstate)
        self.add_event_handler('my_ping', self.myping)
        self.add_event_handler('presence', self.presence)
        self.add_event_handler('notif', self.recv_notif)
        self.add_event_handler('zmq', self.recv_events)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("groupchat_invite", self.accept_invite)

        self.room = room.split(", ") if ", " in room else room
        self.nick = "Jarvis S"
        self.nickSlug = "@Jarvis"
        self._users = {}
        self._controller = Controller()
        self._questions = {}
        self._zmq = None

    def start(self, event):
        self.get_roster()
        self.send_presence()
        if isinstance(self.room, str):
            self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        wait=True)
        else:
            for r in self.room:
                self.plugin['xep_0045'].joinMUC(r,
                                        self.nick,
                                        wait=True)

    def presence(self, event):
        print(str(event))

    def chatstate(self, event):
        print(str(event['body']))
        #composing, paused, inactive

    def accept_invite(self, inv):
       print("Invite from %s to %s" %(inv["from"], inv["to"]))
       self.plugin['xep_0045'].joinMUC(inv["from"], self.nick, wait=True)

    def send_msg(self, message, room=None):
        matched = None
        if not room:
            room = message.exp
        for r in self.room:
            if "%s@" % room.replace(" ", "_") in r:
                matched = r
        self.send_message(mto=message.exp if not room else matched,
                          mbody=message.body,
                          mtype=message.mtype)

    def recv_events(self, message):
        print("recv_events %s" % str(message))
        self.send_msg(message, message.room)

    def recv_notif(self, notif):
        print("recv_notif %s" % notif)
        n = Notif(notif)
        h = HipChat()
        if n.type == "reminder":
            h.sayHtml("@%s, I have to remind you to %s" % (n.to, n.message) if n.to else n.message, n.room)
        elif n.type == "notification":
            h.sayHtml("@%s %s" % (n.to, n.message) if n.to else n.message, n.room)

    def myping(self, event):
        m = self.Message()
        m['to'] = "147982_1068687@chat.hipchat.com"
        m['type'] = "chat"
        m['body'] = " "
        m.send()
        print("ping")

    def muc_message(self, msg):
        if "delay" in msg.keys():
            #print("delayed...")
            pass
        # and self.nickSlug in msg['body']
        elif msg['mucnick'] != self.nick:
            print("muc_message: " + str(msg))
            try:
                #msg['body'] = msg['body'].replace(self.nickSlug, "")
                result = self._controller.do(Msg(msg, self))
                print(str(result))
                if isinstance(result, dict) and "type" in result:
                    if result["type"] == "image":
                        self.send_image(msg["from"], result["image"], mfrom=msg["to"], mtype=msg["type"])
                    else:
                        msg.reply(result).send()
                elif isinstance(result, Question):
                    if msg["from"] not in self._questions:
                        self._questions[msg["from"]] = []
                    self._questions[msg["from"]].append(result)
                    msg.reply(result.message()).send()
                elif result is None:
                    print("ici ???")
                    return
                else:
                    msg.reply(result).send()
            except Exception as e:
                msg.reply("An error occured: %s" % str(e)).send()
            #self.message(msg)
            #self.send_message(mto=msg['from'].bare,
            #                  mbody="I heard that, %s." % msg['mucnick'],
            #                  mtype='groupchat')

    def message(self, msg):
        #print("message: " + str(msg))
        if "delay" in msg.keys():
            pass
        if str(msg["from"]).startswith("147982_"):
            if msg['type'] in ('normal', 'chat'):
                try:
                    # check if question in waiting
                    if msg["from"] in self._questions and len(self._questions[msg["from"]]) > 0:
                        q = self._questions[msg["from"]][0]
                        result = q.answer(msg['body'])
                        if q.answered():
                            del self._questions[msg["from"]][0]
                        #msg.reply(res).send()
                    else:
                        result = self._controller.do(Msg(msg, self))
                    if isinstance(result, dict) and "type" in result:
                        if result["type"] == "image":
                            self.send_image(msg["from"], result["image"], mtype=msg["type"])
                        else:
                            msg.reply(result).send()
                    elif isinstance(result, Question):
                        if msg["from"] not in self._questions:
                            self._questions[msg["from"]] = []
                        self._questions[msg["from"]].append(result)
                        msg.reply(result.message()).send()
                    else:
                        msg.reply(result).send()
                except Exception as e:
                    msg.reply("An error occured: %s" % str(e)).send()



def main():
    auth = Conf("bot.conf").getSection("auth")
    if not "login" in auth or not "password" in auth:
        print("Configuration not entirely filled.. Try again.")
        sys.exit(1)
    xmpp = Jarvis(auth["login"], auth["password"], auth["room"])
    xmpp.ssl_version = ssl.PROTOCOL_SSLv3
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199')
    xmpp.register_plugin('xep_0085') # status message
    xmpp.register_plugin('xep_0071') # Xhtml
    xmpp.register_plugin('xep_0045') # multi user chan
    xmpp.register_plugin('xep_0203')  # XMPP Delayed messages
    xmpp.register_plugin('xep_0249')  # XMPP direct MUC invites
    e = Events(xmpp)
    e.start()
    s = Scheduler(xmpp)
    s.start()
    t = ClientTask(xmpp)
    t.start()

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
    main()