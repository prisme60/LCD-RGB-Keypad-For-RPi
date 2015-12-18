#!/bin/usr/python3
# -*- coding: utf-8 -*-

import sys
from struct import *

class DisplayPacket:

    def __init__(self, user=None, message=None):
        self._user = user
        self._message = message

    def unpack(self, binaryData):
        spaces = ' \t\r\n\x00'
        u, m = unpack('@20s160s', binaryData)
        print('(u,m)=({!r},{!r})'.format(u, m))
        if sys.version > '3':
            self._user, self._message = u.decode('utf-8').rstrip(spaces), m.decode('utf-8').rstrip(spaces)
        else:
            self._user, self._message = u.rstrip(spaces), m.rstrip(spaces)
        print('(user,message)=({!r},{!r})'.format(self.user, self.message))

    def pack(self):
        return pack('@20s160s', self._user.encode('utf-8'), self._message.encode('utf-8'))

    @property
    def user(self):
        return self._user

    @property
    def message(self):
        return self._message


if __name__ == '__main__':
    if sys.version > '3':
        dp = DisplayPacket('cf', 'V\xc3\xa9rification de la gestion des accents')
    else:
        dp = DisplayPacket('cf', 'V\xc3\xa9rification de la gestion des accents')
    binaryData = dp.pack()
    dp2 = DisplayPacket()
    dp2.unpack(binaryData)
    print('user = "{}" message="{}"'.format(dp2.user, dp2.message))
