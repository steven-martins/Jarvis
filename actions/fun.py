__author__ = 'Steven'

import subprocess, requests, random

from actions import Action
from decorators import hear, respond_to

import types

class Coffee(Action.Action):

    @respond_to("(?:some) coffee")
    def run(self, message):
        """ Display outrageous coffee image """
        #return {type:"image", image:}
        #
        data = {
            "q": "coffee",
            "v": "1.0",
            "safe": "active",
            "rsz": "8"
        }
        r = requests.get("http://ajax.googleapis.com/ajax/services/search/images", params=data)
        results = r.json()["responseData"]["results"]
        if len(results) > 0:
            url = random.choice(results)["unescapedUrl"]
            self.sayImage(url, room=message.room)
        else:
            return "you drunk too much coffee."

class DefineMe(Action.Action):
    @respond_to("define me (?P<search_query>.*)$")
    def run(self, message, search_query):
        """ Search a definition for ___, and post a random one"""
        r = requests.get("http://urbanscraper.herokuapp.com/search/%s" % search_query)
        results = r.json()
        print(str(results))
        if len(results) > 0:
            return random.choice(results)["definition"]
        else:
            return "Couldn't find anything!"

class ImageMe(Action.Action):
    @respond_to("image me (?P<search_query>.*)$")
    def run(self, message, search_query):
        """ Search google images for ___, and post a random one"""
        print("imageMe: %s " % search_query)
        #"safe": "off",
        data = {
            "q": search_query,
            "v": "1.0",
            "safe": "active",
            "rsz": "8"
        }
        r = requests.get("http://ajax.googleapis.com/ajax/services/search/images", params=data)
        results = r.json()["responseData"]["results"]
        if len(results) > 0:
            url = random.choice(results)["unescapedUrl"]
            print(str(url))
            return "%s" % url
        else:
            return "Couldn't find anything!"
