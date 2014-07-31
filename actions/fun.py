__author__ = 'Steven'

import subprocess, requests, random

from actions import Action
from decorators import hear, respond_to

class Coffee(Action.Action):

    @respond_to("(?:some) coffee")
    def run(self, *args, **kwargs):
        """ Display outrageous coffee image """
        #return {type:"image", image:}
        #return {"type": "image", "image": "me.png"}
        self.sayImage("http://i.telegraph.co.uk/multimedia/archive/02679/coffee_2679924b.jpg")
        #return """My turn!
        #        http://i.telegraph.co.uk/multimedia/archive/02679/coffee_2679924b.jpg
        #        """


class DefineMe(Action.Action):
    @respond_to("define me (?P<search_query>.*)$")
    def run(self, params, search_query, *args, **kwarfs):
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
    def run(self, params, search_query, *args, **kwargs):
        """ Search google images for ___, and post a random one"""
        print("imageMe: %s " % search_query)
        #"safe": "active",
        data = {
            "q": search_query,
            "v": "1.0",
            "safe": "off",
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

#class Downloader(Action.Action):
#    def run(self, *args:
#        subprocess.Popen()
