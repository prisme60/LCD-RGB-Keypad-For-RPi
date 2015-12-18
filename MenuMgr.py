#!/usr/bin/python
# -*- coding: utf-8 -*-

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import convertAccentCharutf8
from GlyphSprites import Sprites

import urllib
import urllib2

class MenuMgr:
    index = 0
    menu_need_refresh = True

    def __init__(self):
        self.index = 0

    def next_item(self):
        self.menu_need_refresh = True
        self.index = (self.index + 1) % len(self.menu)

    def prev_item(self):
        self.menu_need_refresh = True
        self.index = (self.index + len(self.menu) - 1) % len(self.menu)

    def get_text(self):
        """ returns the text menu to display """
        (text, func) = self.menu[self.index]
        self. menu_need_refresh = False
        return text

    def execute_item(self, lcd):
        """ returns a text of the result """
        (text, func) = self.menu[self.index]
        return func(self, lcd)

    def Activate_WIFI(self, lcd):
        assert isinstance(lcd, Adafruit_CharLCDPlate)
        req = urllib2.urlopen('http://localhost:8082/wlanON')
        html = req.read()
        return html

    def Disable_WIFI(self, lcd):
        assert isinstance(lcd, Adafruit_CharLCDPlate)
        req = urllib2.urlopen('http://localhost:8082/wlanOFF')
        html = req.read()
        return html

    def WIFI_State(self, lcd):
        assert isinstance(lcd, Adafruit_CharLCDPlate)
        req = urllib2.urlopen('http://localhost:8082/wlan')
        html = req.read()
        return html

    def Msg_To_Ch(self, lcd):
        assert isinstance(lcd, object)
        data = urllib.urlencode({'msg': 'Message venant de rp1 pour Christian'})
        req = urllib2.urlopen('http://localhost:8082/writeMsg', data)
        html = req.read()
        return html

    def Msg_To_MF(self, lcd):
        assert isinstance(lcd, object)
        data = urllib.urlencode({'msg': 'Message venant de rp1 pour Marie-France'})
        req = urllib2.urlopen('http://localhost:8082/writeMsg', data)
        html = req.read()
        return html

    menu = [
        ("Active WIFI", Activate_WIFI),
        ("Désactive WIFI", Disable_WIFI),
        ("Etat WIFI", WIFI_State),
        ("Prévenir Ch.", Msg_To_Ch),
        ("Prévenir MF", Msg_To_MF)
    ]
