# switchbox: map switches to mouse and keyboard events
# https://github.com/dhalbert/switchbox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2017 by Daniel C. Halbert
#
# event_names.py:
# Map names to corresponding keycodes and mouse events.

from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# These functions are used as mouse events, and called with a Mouse device.
def leftclick(mouse):
    mouse.click(Mouse.LEFT_BUTTON)

def middleclick(mouse):
    mouse.click(Mouse.MIDDLE_BUTTON)

def rightclick(mouse):
    mouse.click(Mouse.RIGHT_BUTTON)

def scrollin(mouse):
    mouse.move(0, 0, -1)

def scrollout(mouse):
    mouse.move(0, 0, 1)


EVENT_NAMES = {
    "alt" : Keycode.ALT,
    "cmd" : Keycode.GUI,
    "ctrl" : Keycode.CONTROL,
    "option" : Keycode.ALT,
    "shift" : Keycode.SHIFT,
    "windows" : Keycode.GUI,
    
    # Characters that have special meanings in the mappings file.
    # Use these names instead.
    "minus" : Keycode.MINUS,
    "space" : Keycode.SPACE,

    # Use shift-' for doublequote (")

    "enter" : Keycode.ENTER,
    "backspace" : Keycode.BACKSPACE,
    "tab" : Keycode.TAB,
    "capslock" : Keycode.CAPS_LOCK,

    "delete" : Keycode.DELETE,
    "end" : Keycode.END,
    "home" : Keycode.HOME,
    "insert" : Keycode.INSERT,
    "pagedown" : Keycode.PAGE_DOWN,
    "pageup" : Keycode.PAGE_UP,

    "leftarrow" : Keycode.LEFT_ARROW,
    "rightarrow" : Keycode.RIGHT_ARROW,
    "uparrow" : Keycode.UP_ARROW,
    "downarrow" : Keycode.DOWN_ARROW,

    "leftclick" : leftclick,
    "middleclick" : middleclick,
    "rightclick" : rightclick,
    "scrollin" : scrollin,
    "scrollout" : scrollout,
}

    

    
    

