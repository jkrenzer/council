# -*- coding: utf-8 -*-
import council.moduleHandling.module as module

class Log(module.Class):
    _name="log"
    def debug(self, text):
        print("Debug: %s" % text)
    def notice(self, text):
        print("Notice: %s" % text)
    def warning(self, text):
        print("Warning: %s" % text)
    def error(self, text):
        print("Error: %s" % text)
