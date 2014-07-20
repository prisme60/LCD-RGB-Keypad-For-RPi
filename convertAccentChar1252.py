#!/usr/bin/python
# -*- coding: cp1252 -*-

import sys


def enc(letter):
    return letter.encode('utf-8').decode('cp1252')


dictGlyph = {
    enc('é') : ('e',
          [0b00100,
           0b01000,
           0b01110,
           0b11011,
           0b11111,
           0b11000,
           0b01111,
           0b00000]),
    'è' : ('e',
          [0b01000,
           0b00100,
           0b01110,
           0b11011,
           0b11111,
           0b11000,
           0b01111,
           0b00000]),
    'ê' : ('e',
          [0b00100,
           0b01010,
           0b01110,
           0b11011,
           0b11111,
           0b11000,
           0b01111,
           0b00000]),
    'ë' : ('e',
          [0b01010,
           0b00000,
           0b01110,
           0b11011,
           0b11111,
           0b11000,
           0b01111,
           0b00000]),
    'É' : ('E',None),
    'È' : ('E',None),
    'Ê' : ('E',None),
    'Ë' : ('E',None),
    'à' : ('a',
          [0b00000,
           0b00000,
           0b01110,
           0b00011,
           0b01111,
           0b11011,
           0b01111,
           0b00000]),
    'À' : ('A',None),
    'ù' : ('u',
          [0b00000,
           0b00000,
           0b10001,
           0b10001,
           0b10001,
           0b10001,
           0b01111,
           0b00000]),
    'ô' : ('o',
          [0b00000,
           0b00000,
           0b01110,
           0b10001,
           0b10001,
           0b10001,
           0b01110,
           0b00000]),
    'Ô' : ('O', None)
}

def convertMsg(message):
    return convertMsgParam(message, [], [])

def convertMsgParam(message,glyphList,charList):
    """ return message and glyph list """
    newMsg = ''

    for c in message:
        print("read c =" + c)
        if c in dictGlyph:
            if c in charList: #glyph has already been added to the list, so use it!
                newMsg += chr(charList.index(c))
            else:
                glyphTuple = dictGlyph[c]
                if glyphTuple[1] != None: # is a glyph defined ?
                    glyphList.append(dictGlyph[c])
                    charList.append(c)
                    newMsg += chr(len(glyphList))
                else:
                    newMsg += glyphTuple[0] #use replacement char (because there is no glyph) 
        else:
            newMsg += c #add normal char to the message
    return (newMsg,glyphList,charList)


if __name__ == '__main__':
    print(repr(dictGlyph))
    if len(sys.argv) > 1:
        print(repr(convertMsg(" ".join(sys.argv[1:]).decode('utf-8').encode('cp1252'))))
    else:
        print(repr(convertMsg('Accents du a : à\nAccents du e: éèëÈÉÊË\nAccents du u: ù\nAccents du o : ôÔ')))

