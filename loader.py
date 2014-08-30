#!/usr/bin/python

import logging, string
import fileinput
try:
    from ConfigParser import ConfigParser, Error, NoOptionError
except:
    from configparser import ConfigParser, Error, NoOptionError
import os

class Conf:
    def __init__(self, filename):
        self._filename = filename
        self._config = ConfigParser()
        try:
            self._config.read(os.path.expanduser(filename))
        except Exception as e:
            logging.error("[Conf]" + self._filename + ": " + str(e))
            raise Exception("Error during loading file " + self._filename)

    def getSection(self, section):
        data={}
        try:
            if section in self._config.sections():
                for name, value in self._config.items(section):
                    data[name] = value
        except Exception as e:
            logging.error("[Conf]" + self._filename + ": " + str(e))
        for key, value in data.items():
            if ", " in value:
                data[key] = value.split(", ")
        return data

    def get(self, section, option, default=""):
        val = default
        try:
            val = self._config.get(section, option)
        except:
            val = default
        if ", " in val:
            return string.split(val, ", ")
        return default

    def sections(self):
        return self._config.sections()
    
    def getAll(self):
        data = {}
        for section in self.sections():
            data[section] = self.getSection(section)
        return data
