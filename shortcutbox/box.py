# https://github.com/dhalbert/ShortcutBox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2018 by Daniel C. Halbert

"""
Adaptive switch control for emulation of mouse and keyboard events (shortcuts).

Each switch cycles through a list of mappings. One switch is a "do it" button,
which sends the mapping for the most recently selected mapping.

Switch mappings are not hardwired. The settings are read from the file
`shortcuts.txt`, stored in the local filesystem.

shortcuts.txt example:

1 CONTROL-X ; cut
1 CONTROL-C ; copy
1 CONTROL-V ; paste

2 LEFT_BUTTON LEFT_BUTTON ; dbl-click
2 RIGHT_BUTTON ; right-click
2 LEFT_BUTTON HOLD_MOUSE ; left-hold
2 RELEASE ; release mouse buttons

3 CONTROL-SHIFT-K ; ctrl-shift-k

4 T H E ; the
4 A N D ; and
4 PERIOD ; .
4 SPACE ; space
"""

import time

import digitalio
import board

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl

from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

from shortcutbox.shortcuts import Shortcut, BadShortcut


# Wait BOUNCE_SECS to make sure switch has finished bouncing
BOUNCE_SECS = 0.100

# Switch number that executes mapping
DO_IT_SWITCH = 0

# Don't use D13: it's connected to the blinky LED and will get pulled down.
# Use A1 instead. A0 has the DAC, which might be useful for something later.
# There are seven 3.5mm jacks on the switch box. D5 is the do-it switch.
SWITCH_PINS = (board.D5, board.D6, board.D9, board.D10, board.D11, board.D12, board.A1)

class ShortcutBox:
    """Convert switch presses to keyboard and mouse shortcuts."""
    def __init__(self, filename="shortcuts.txt"):
        self.display = LCD(I2CPCF8574Interface(0x27))
        self.display.clear()

        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.consumer_control = ConsumerControl()

        self.display.print("Ready! Choose a\nshortcut and press\nthe do-it switch.")

        self.switch_ins = tuple(digitalio.DigitalInOut(pin) for pin in SWITCH_PINS)
        for switch_in in self.switch_ins:
            switch_in.switch_to_input(pull=digitalio.Pull.UP)

        try:
            # Shortcuts is a dict mapping a switch number to a list of Shortcuts.
            self.shortcuts = Shortcut.read_shortcuts(filename)
        except BadShortcut as ex:
            self.fatal_error(*ex.args)

        if not self.shortcuts:
            self.fatal_error("No shortcuts defined!")

        self.current_switch = None

        # Keep track of the current shortcut for each switch. Start at the zero-th ones.
        # Skip any switches with no shortcuts.
        self.current_shortcut_index = {}
        for switch in self.shortcuts:
            self.current_shortcut_index[switch] = 0


    def run(self):
        """Start shortcut processing. Run forever."""
        while True:
            for switch, switch_in in enumerate(self.switch_ins):
                if not switch_in.value:
                    # If switch is pressed, it's pulled low. Debounce by waiting for bounce time.
                    time.sleep(BOUNCE_SECS)
                    if switch == DO_IT_SWITCH and self.current_switch:
                        self.execute(self.current_shortcut)
                        self.display.print(" *")
                    else:
                        if switch == self.current_switch:
                            # Advance to next shortcut if this not the first press on this switch.
                            self.next_shortcut(switch)
                        else:
                            # Change to a new switch. Don't advance that switch's shortcuts yet.
                            self.current_switch = switch
                        self.display_shortcut(self.current_shortcut, switch)
                    # Wait for switch to be released.
                    while not switch_in.value:
                        pass


    @property
    def current_shortcut(self):
        """The last shortcut designated by a switch press, or None if we're on a switch with no shortcuts."""
        switch = self.current_switch
        if switch in self.shortcuts:
            return self.shortcuts[switch][self.current_shortcut_index[switch]]
        else:
            return None

    def execute(self, shortcut):
        """Execute the given shortcut, if it's not None."""
        if shortcut:
            shortcut.execute(self.keyboard, self.mouse, self.consumer_control)

    def next_shortcut(self, switch):
        """Move on to the next shortcut for the given switch. Skip switches with no shortcuts."""
        if switch in self.current_shortcut_index:
            self.current_shortcut_index[switch] = (
                (self.current_shortcut_index[switch] + 1) % len(self.shortcuts[switch]))

    def display_shortcut(self, shortcut, switch):
        self.display.clear()
        self.display.print(str(switch), ' ', shortcut.label if shortcut
                           else "No shortcuts\non this switch!")

    def fatal_error(self, *strings):
        """Display and error and hang until reset."""
        self.display.clear()
        self.display.print(' '.join(strings))
        # Hang until user presses the reset button.
        while True:
            pass
