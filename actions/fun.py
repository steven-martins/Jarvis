__author__ = 'Steven'

import subprocess, requests, random

from . import Action

class Coffee(Action.Action):
    """ Turn coffee into code"""
    def run(self, *args):
        #return {type:"image", image:"http://i.telegraph.co.uk/multimedia/archive/02679/coffee_2679924b.jpg"}
        return {"type": "image", "image": "me.png"}
        #return """I turn <b>coffee</b> into code, like you!
#"""

class ImageMe(Action.Action):
    """ Search google images for ___, and post a random one"""
    def run(self, params, search_query, *args, **kwargs):
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
            return "%s" % url
        else:
            return "Couldn't find anything!"

#class Downloader(Action.Action):
#    def run(self, *args:
#        subprocess.Popen()


class Tea(Action.Action):
    """ Give some tea at five o'clock only!"""
    def run(self, *args):
        return """It's to early! Try again around 5 o'clock.
"""
