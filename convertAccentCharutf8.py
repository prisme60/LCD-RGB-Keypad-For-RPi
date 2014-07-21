#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from GlyphSprites import Sprites


def enc(letter):
    return letter.encode('cp1252')


dictGlyph = {
    enc(u'é') : ('e',Sprites.letterEacute),
    enc(u'è') : ('e',Sprites.letterEgrave),
    enc(u'ê') : ('e',Sprites.letterEcirc),
    enc(u'ë') : ('e',Sprites.letterEuml),
    enc(u'É') : ('E',None),
    enc(u'È') : ('E',None),
    enc(u'Ê') : ('E',None),
    enc(u'Ë') : ('E',None),
    enc(u'à') : ('a',Sprites.letterAgrave),
    enc(u'À') : ('A',None),
    enc(u'ù') : ('u',Sprites.letterUgrave),
    enc(u'ô') : ('o',Sprites.letterOcirc),
    enc(u'Ô') : ('O', None)
}

maxCustomChar = 8

def convertMsg(message):
    return convertMsgParam(message, [], [], maxCustomChar)

def convertMsgParam(message,glyphList,charList,maxChar):
    """ return message and glyph list """
    newMsg = ''
    offsetGlyphList = len(glyphList) - len(charList) 

    for c in message:
        print("read c =" + c)
        if c in dictGlyph:
            if c in charList: #glyph has already been added to the list, so use it!
                newMsg += chr(offsetGlyphList + charList.index(c))
            else:
                glyphTuple = dictGlyph[c]
                if len(glyphList) < maxChar and glyphTuple[1] != None: # is there still a free place? is a glyph defined ?
                    glyphList.append(glyphTuple[1])
                    charList.append(c)
                    newMsg += chr(len(glyphList)-1)
                else:
                    newMsg += glyphTuple[0] #use replacement char (because there is no glyph or because there is no more place for custom char) 
        else:
            newMsg += c #add normal char to the message
    return (newMsg,glyphList,charList)


if __name__ == '__main__':
    print(repr(dictGlyph))
    if len(sys.argv) > 1:
        print(repr(convertMsg(" ".join(sys.argv[1:]).decode('utf-8').encode('cp1252'))))
    else:
        print(repr(convertMsg(enc(u'Accents du a : à\nAccents du e: éèëÈÉÊË\nAccents du u: ù\nAccents du o : ôÔ'))))

