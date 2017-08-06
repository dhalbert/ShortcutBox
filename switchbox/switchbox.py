# switchbox: map switches to mouse and keyboard events
# https://github.com/dhalbert/switchbox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2017 by Daniel C. Halbert

# switchbox.py:
# Adaptive switch control for emulation of mouse and keyboard.
#
# One switch cycles through "pages" of mappings of all the other switches.
#
# Switch mappings are not hardwired. The settings are read from the file:
# switches.txt, stored in the local filesystem.
#
# switches.txt example:
"""
page-1 "common"
switch-1 "cut" ctrl-x
switch-2 "copy" ctrl-c
switch-3 "paste"
switch-4 "[rightmouse]" rightclick

# This is a comment.
page-2 "examples"
switch-1 "the" t h e
switch-2 "[leftmouse][leftmouse]" leftclick leftclick
switch-3 "c-s-k" ctrl-shift-k
switch-4 "[shift][leftmouse]" shift-leftclick
"""

from switchbox.mappings import Mappings
from switchbox.display import Display

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

import digitalio
from board import *
import time

class Switchbox:
    # Wait _BOUNCE_MSECS to make sure switch has finished bouncing
    BOUNCE_SECS = 0.200 # 100 msecs

    # Switch number that changes pages.
    PAGE_SWITCH = const(0)
    
    def __init__(self, switches_file="switches.txt"):
        self.display = Display()
        self.display.clear()
        self.keyboard = Keyboard()
        self.mouse = Mouse()

        try:
            self.mappings = Mappings(switches_file)
            self.page_index = 0
            self.display_page()
        except BadMapping as e:
            fatal_error(*e.args, "Fix and reset.")

        self.switch_inputs = [digitalio.DigitalInOut(pin) for pin in (D5, D6, D10, D11, D12, D13, A0, A1, A2, A3, A4, A5)]
        for switch_input in self.switch_inputs:
            switch_input.switch_to_input(pull=digitalio.Pull.UP)

    def run(self):
        while True:
            for switch_num, switch_input in enumerate(self.switch_inputs):
                if not switch_input.value:
                    # switch pressed - pulled low. Wait for bounce time and see if it's still low.
                    time.sleep(self.BOUNCE_SECS)
                    print("pressed", switch_num, time.monotonic())
                    if not switch_input.value:
                        if switch_num == self.PAGE_SWITCH:
                            self.next_page()
                        else:
                            self.press_switch(switch_num)

    def next_page(self):
        # Advance to next page. Wrap around if necessary.
        # Note that the page index does not correspond to the page number.
        self.page_index = (self.page_index + 1) % len(self.mappings.pages)
        self.display.clear()

    def display_page(self):
        page = self.mappings.pages[self.page_index]
        self.display.print(page.desc())
        self.display.print("\n")
        for switch in page.switches:
            self.display.print(switch.desc())
            self.display.print(" ")

    def press_switch(self, switch_num):
        # Find switch number on current page and send its events.
        # Skip if there is no such switch defined.
        for switch in self.mappings.pages[self.page_index].switches:
            if switch.switch_num == switch_num:
                self.send_events(switch.events)
                return

    def send_events(events):
        for event in events:
            for item in event:
                if isinstance(item, int):
                    self.keyboard.press(item)
                elif callable(item):
                    item(self.keyboard, self.mouse)
                else:
                    fatal_error("bad event:", event)
                    keyboard.release_all()

    def fatal_error(strings):
        self.display.clear()
        self.display.print(*strings)
        # Hang until user presses the reset button.
        while True:
            pass
        
