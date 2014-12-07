#!/usr/bin/python
# -*- coding: utf-8 -*-


from time import sleep
import copy
import atexit
import sys
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import convertAccentCharutf8 
from GlyphSprites import Sprites
from recvMsgToDisplay import RecvMsg

if len(sys.argv) >= 2:
    sock_path = sys.argv[1]
else:
    sock_path = "/run/lcd/socket"

print('Use socket : ' + sock_path)

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()
atexit.register(lcd.stop)
lcd.backlight(True)


lcd.createChar(0,Sprites.horizontalLines)

# Clear display and show greeting, pause 1 sec
lcd.clear()
lcd.message("Adafruit RGB LCD\nPlate w/Keypad!\x00")
sleep(1)

# Cycle through backlight colors
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.WHITE, lcd.OFF)
for c in col:
    lcd.ledRGB(c)
    sleep(.5)

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  , u'\x00Vin très rouge à boire dans le vignoble du chateau', lcd.RED, [Sprites.horizontalLines]),
       (lcd.UP    , u'\x00  Sita sings  \x01\n\x00  the blues   \x01'  , lcd.BLUE , [Sprites.musicalNote,Sprites.bellSymbol]),
       (lcd.DOWN  , u'\x00see fields\n\x00 of green'                   , lcd.GREEN, [Sprites.bellSymbol]),
       (lcd.RIGHT , u'Purple mountain\nmajesties\x00\x01\x02'          , lcd.VIOLET,[Sprites.hourglassFull,Sprites.hourglassMid,Sprites.hourglassEmpty]),
       (lcd.SELECT, u''                                                , lcd.WHITE, []))
buttonState = 0
rm = RecvMsg(sock_path)
ledBlink, ledColor, ledGreenPulseModulo = False, lcd.OFF, 0
while True:
    lcd.scrollDisplayLeft()
    previousButtonState = buttonState
    buttonState = lcd.buttons()
    if previousButtonState != buttonState:
        if (buttonState & (1 << lcd.SELECT)) != 0:
            b = lcd.SELECT
            print('SELECT button')
            if ledBlink:
               ledBlink = False
            else:
               lcd.backlight(False)
            #(convertedMessage,glyphList,charList) = convertAccentCharutf8.convertMsg(b[1].encode('cp1252'),copy.deepcopy(b[3]),[],8)
            #print(repr((convertedMessage,glyphList,charList)))
            #for (i,glyph) in enumerate(glyphList) : #copy glyphs to the LCD memory (b[3] + accent chars)
            #    lcd.createChar(i, glyph)
            #sleep(.5)
            #print(b[1])
            #lcd.clear()
            #lcd.message(convertedMessage)
            #lcd.ledRGB(b[2])
            #ledBlink = False
            #sleep(2)
            #lcd.clear()
            #lcd.message('Displays special\n\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09|||||||')
    #look in the socket if there is a message to display!
    (user,message) = rm.recvMsg(0.1)
    if user != None and message != None:
        print(message)
        (convertedMessage,glyphList,charList) = convertAccentCharutf8.convertMsg(message.decode('utf-8').encode('cp1252'))
        print(repr((convertedMessage,glyphList,charList)))
        for (i,glyph) in enumerate(glyphList) : #copy glyphs to the LCD memory (accent chars)
            lcd.createChar(i, glyph)
        lcd.clear()
        lcd.message(convertedMessage)
        lcd.backlight(True)
        ledBlink = True
	ledColor = lcd.RED
    #Manage led blink (about 10Hz)
    if ledBlink:
        lcd.ledRGB(ledColor)
	ledColor = (~ledColor) & lcd.WHITE
    elif ledGreenPulseModulo % 100 == 0:
        lcd.ledRGB(lcd.GREEN)
    else:
        lcd.ledRGB(lcd.OFF)
    ledGreenPulseModulo+=1
