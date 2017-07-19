# switchbox: map switches to mouse and keyboard events
# https://github.com/dhalbert/switchbox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2017 by Daniel C. Halbert
#
# events.py:
# Map names to corresponding keycodes and mouse events.

from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# Events are either integers, which are keycodes, or functions, which are called
# with mouse and keyboard arguments.

# Currently there are no functions that use the keyboard arguments

def leftclick(keyboard, mouse):
    mouse.click(Mouse.LEFT_BUTTON)

def middleclick(keyboard, mouse):
    mouse.click(Mouse.MIDDLE_BUTTON)

def rightclick(keyboard, mouse):
    mouse.click(Mouse.RIGHT_BUTTON)

def scrollin(keyboard, mouse):
    mouse.move(0, 0, -1)

def scrollout(keyboard, mouse):
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
    "space" : Keycode.SPACEBAR,

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
            
            

    

    
    

