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

class Events(Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self._bot = bot

    def run(self):
        while 1:
            print("thread")
            obj = {}
            obj["type"] = "notification"
            obj["to"] = "@gmail.com"
            #self._bot.event('my_event', obj)
            time.sleep(15)


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')


class Jarvis(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super(Jarvis, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('chatstate', self.chatstate)
        self.add_event_handler('my_event', self.myevent)
        self.add_event_handler('presence', self.presence)
        self._users = {}
        self._controller = Controller()
        self._questions = {}

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def presence(self, event):
        print(str(event))


    def chatstate(self, event):
        print(str(event['body']))
        #composing, paused, inactive

    def myevent(self, event):
        print(str(event))
        #self.send_message(mto="", mbody=event["type"], mtype="chat")

    def send_image(self, jid, img_url):
        m = self.Message()
        m['to'] = jid
        m['type'] = 'chat'
        m['body'] = 'Tried sending an image using OOB'
        m['oob']['url'] = img_url
        m.send()

    #def send_image(self, jid, img_file_path):
    #    m = self.Message()
    #    m['to'] = jid
    #    m['type'] = 'chat'
    #    with open(img_file_path, 'rb') as img_file:
    #        img = img_file.read()
    #    if img:
    #        cid = self['xep_0231'].set_bob(img, 'image/png')
    #        m['body'] = 'Tried sending an image using BOB'
    #        m['html']['body'] = '<img src="cid:%s" />' % cid
    #        print(str(m))
    #        m.send()

    def message(self, msg):
        print(str(msg))
        if str(msg["from"]).startswith("steven.martins."):
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
                        result = self._controller.do(msg['body'])
                    if isinstance(result, types.DictType) and "type" in result:
                        if result["type"] == "image":
                            self.send_image(msg["from"], result["image"])
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
    xmpp = Jarvis(auth["login"], auth["password"])
    xmpp.ssl_version = ssl.PROTOCOL_SSLv3
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199')
    xmpp.register_plugin('xep_0085') # status message
    xmpp.register_plugin('xep_0066') # Image : OOB
    #xmpp.register_plugin('xep_0045') # multi user chan

    e = Events(xmpp)
    e.start()

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
    main()