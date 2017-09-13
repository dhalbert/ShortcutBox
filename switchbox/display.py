# switchbox: map switches to mouse and keyboard events
# https://github.com/dhalbert/switchbox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2017 by Daniel C. Halbert
#
# display.py:
# Switchbox display: 20x4 character LCD

from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

class Display:
    
    _SPECIAL_CHAR_NAMES = {
        "\\" : '\x05',
        "[uparrow]" : '\x06',
        "[downarrow]" : '\x07',
        "[rightarrow]" : '\x7e',
        "[leftarrow]" : '\x7f',
        }

    _BACKSLASH_BITMAP = bytearray((
        0b00000,
        0b10000,
        0b01000,
        0b00100,
        0b00010,
        0b00001,
        0b00000,
        0b00000))

    _UPARROW_BITMAP = bytearray((
        0b00100,
        0b01110,
        0b10101,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00000))

    _DOWNARROW_BITMAP = bytearray((
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b10101,
        0b01110,
        0b00100,
        0b00000))

    def __init__(self):
        self.lcd = LCD(I2CPCF8574Interface(0x27))
        self.lcd.create_char(ord(self._SPECIAL_CHAR_NAMES['\\']), self._BACKSLASH_BITMAP)
        self.lcd.create_char(ord(self._SPECIAL_CHAR_NAMES['[uparrow]']), self._UPARROW_BITMAP)
        self.lcd.create_char(ord(self._SPECIAL_CHAR_NAMES['[downarrow]']), self._DOWNARROW_BITMAP)

    def remap_special_chars(self, s):
        """Map [xxx] names and a few other characters to correct entries for character generator."""
        for orig, subst in self._SPECIAL_CHAR_NAMES.items():
            s = s.replace(orig, subst)
        return s

    def print(self, s):
        self.lcd.print(self.remap_special_chars(s))

    def clear(self):
        self.lcd.clear()

