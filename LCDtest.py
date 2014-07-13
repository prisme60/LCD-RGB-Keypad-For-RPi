#!/usr/bin/python

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import atexit

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()
atexit.register(lcd.stop)
lcd.backlight(True)

# Clear display and show greeting, pause 1 sec
lcd.clear()
lcd.message("Adafruit RGB LCD\nPlate w/Keypad!")
sleep(1)

# Cycle through backlight colors
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.WHITE, lcd.OFF)
for c in col:
    lcd.ledRGB(c)
    sleep(.5)

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  , 'Red Red Wine'              , lcd.RED),
       (lcd.UP    , 'Sita sings\nthe blues'     , lcd.BLUE),
       (lcd.DOWN  , 'I see fields\nof green'    , lcd.GREEN),
       (lcd.RIGHT , 'Purple mountain\nmajesties', lcd.VIOLET),
       (lcd.SELECT, ''                          , lcd.WHITE))
prev = -1
while True:
    sleep(.1)
    buttonState = lcd.buttons()
    for b in btn:
        if (buttonState & (1 << b[0])) != 0:
            if b is not prev:
                print b[1]
                lcd.clear()
                lcd.message(b[1])
                lcd.ledRGB(b[2])
                prev = b
            break
