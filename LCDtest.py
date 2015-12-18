#!/usr/bin/python
# -*- coding: utf-8 -*-


from time import sleep
import copy
import atexit
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import convertAccentCharutf8
from GlyphSprites import Sprites

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()
atexit.register(lcd.stop)
lcd.backlight(True)

lcd.createChar(0, Sprites.horizontalLines)

# Clear display and show greeting, pause 1 sec
lcd.clear()
lcd.message("Adafruit RGB LCD\nPlate w/Keypad!\x00")
sleep(1)

# Cycle through backlight colors
col = (lcd.RED, lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.WHITE, lcd.OFF)
for c in col:
    lcd.ledRGB(c)
    sleep(.5)

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT, u'\x00Vin très rouge à boire dans le vignoble du chateau', lcd.RED, [Sprites.horizontalLines]),
       (lcd.UP, u'\x00  Sita sings  \x01\n\x00  the blues   \x01', lcd.BLUE, [Sprites.musicalNote, Sprites.bellSymbol]),
       (lcd.DOWN, u'\x00see fields\n\x00 of green', lcd.GREEN, [Sprites.bellSymbol]),
       (lcd.RIGHT, u'Purple mountain\nmajesties\x00\x01\x02', lcd.VIOLET,
        [Sprites.hourglassFull, Sprites.hourglassMid, Sprites.hourglassEmpty]),
       (lcd.SELECT, u'', lcd.WHITE, []))
prev = -1
while True:
    sleep(.1)
    lcd.scrollDisplayLeft()
    buttonState = lcd.buttons()
    for b in btn:
        if (buttonState & (1 << b[0])) != 0:
            if b is not prev:
                (convertedMessage, glyphList, charList) = convertAccentCharutf8.convertMsg(b[1].encode('cp1252'),
                                                                                           copy.deepcopy(b[3]), [], 8)
                print(repr((convertedMessage, glyphList, charList)))
                for (i, glyph) in enumerate(glyphList):  # copy glyphs to the LCD memory (b[3] + accent chars)
                    lcd.createChar(i, glyph)
                sleep(.5)
                print(b[1])
                lcd.clear()
                lcd.message(convertedMessage)
                lcd.ledRGB(b[2])
                # sleep(2)
                #lcd.clear()
                #lcd.message('Displays special\n\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09|||||||')
                prev = b
            break
