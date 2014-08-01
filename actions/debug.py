__author__ = 'Steven'

import subprocess, requests, random, re

from actions import Action
from decorators import hear, respond_to, one_to_one


class Debug(Action.Action):

    @respond_to("who am I ?")
    def who_am_i(self, message):
        return str(message.mfrom)

    @respond_to("(in)?( )?what room are we ?")
    def who_am_i(self, message):
        return message.room

    @respond_to("display my message")
    def display_my_message(self, message):
        return str(message)

    @one_to_one("display my message")
    def display_my_message_solo(self, message):
        return str(message)

    @respond_to("display an image")
    def display_an_image(self, message):
        self.sayImage("http://screenshots.fr.sftcdn.net/fr/scrn/76000/76332/free-looney-tunes-snowy-holiday-screensaver-2.jpg", room=message.room)

    @one_to_one("display an image")
    def display_an_image_solo(self, message):
        self.sayImage("http://screenshots.fr.sftcdn.net/fr/scrn/76000/76332/free-looney-tunes-snowy-holiday-screensaver-2.jpg", room=message.room)
