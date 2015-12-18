#!/usr/bin/python
# -*- coding: utf-8 -*-


from time import sleep
import atexit
import sys
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import convertAccentCharutf8 
from GlyphSprites import Sprites
from recvMsgToDisplay import RecvMsg
from MenuMgr import MenuMgr


def display_message(lcd, message):
    print(message)
    (convertedMessage, glyphList, charList) = convertAccentCharutf8.convertMsg(message.decode('utf-8').encode('cp1252'))
    print(repr((convertedMessage, glyphList, charList)))
    for (i, glyph) in enumerate(glyphList):  # copy glyphs to the LCD memory (accent chars)
        lcd.createChar(i, glyph)
    lcd.clear()
    lcd.message(convertedMessage)
    lcd.backlight(True)


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


lcd.createChar(0, Sprites.horizontalLines)

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
buttonState = 0
rm = RecvMsg(sock_path)
ledBlink, ledColor, ledGreenPulseModulo = False, lcd.OFF, 0
menu_manager = MenuMgr()
while True:
    lcd.scrollDisplayLeft()
    previousButtonState = buttonState
    buttonState = lcd.buttons()
    if previousButtonState != buttonState:
        if (buttonState & (1 << lcd.SELECT)) != 0:
            print('SELECT button')
            if ledBlink:
                ledBlink = False
            else:
                lcd.backlight(False)
        if (buttonState & (1 << lcd.DOWN)) != 0:
            print('DOWN button')
            lcd.backlight(True)
            menu_manager.next_item()
        if (buttonState & (1 << lcd.UP)) != 0:
            print('UP button')
            lcd.backlight(True)
            menu_manager.prev_item()
        if (buttonState & (1 << lcd.RIGHT)) != 0:
            print('RIGHT button')
            lcd.backlight(True)
            display_message(lcd, menu_manager.execute_item(lcd))
        if menu_manager.menu_need_refresh:
            print('Refresh Menu')
            lcd.backlight(True)
            display_message(lcd, menu_manager.get_text())
                    
    #look in the socket if there is a message to display!
    (user, message) = rm.recvMsg(0.1)
    if user is not None and message is not None:
        display_message(lcd, message)
        ledBlink = True
        ledColor = lcd.RED
    # Manage led blink (about 10Hz)
    if ledBlink:
        lcd.ledRGB(ledColor)
        ledColor = (~ledColor) & lcd.WHITE
    elif ledGreenPulseModulo % 100 == 0:
        lcd.ledRGB(lcd.GREEN)
    else:
        lcd.ledRGB(lcd.OFF)
    ledGreenPulseModulo += 1
