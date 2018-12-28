# https://github.com/dhalbert/ShortcutBox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2018 by Daniel C. Halbert
#
# mappings.py:
# Read mappings.py and convert to internal format.

import ure

from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control_code import ConsumerControlCode

# switch_number EVENT-EVENT EVENT EVENT ; descriptive label
# e.g.:
# 2 SHIFT-T H E ; The

# The event names can be lower-case; they are upper-cased internally.
# 2 shift-t h e ; The

# Remove flag bits.
_EVENT_MASK = 0xffff
_KEYBOARD_EVENT = 0x10000
_MOUSE_EVENT = 0x20000
# Or'd with a ConsumerControlCode.
_CONSUMER_CONTROL_EVENT = 0x40000
# Events that need special handling:
# Don't release keys or mouse buttons when done.
_MOUSE_HOLD = 0x80001
_KEYBOARD_HOLD = 0x80002
# Scroll wheel events.
_MOUSE_SCROLL_IN = 0x80010
_MOUSE_SCROLL_OUT = 0x8011

_RENAMES = {
    "CMD" : "GUI"
    }

_OTHER_EVENTS = {
    # Press a mouse button.
    "LEFT" : _MOUSE_EVENT | Mouse.LEFT_BUTTON,
    "MIDDLE" : _MOUSE_EVENT | Mouse.LEFT_BUTTON,
    "RIGHT" : _MOUSE_EVENT | Mouse.RIGHT_BUTTON,
    # Move the scroll wheel.
    "SCROLL_IN" : _MOUSE_SCROLL_IN,
    "SCROLL_OUT" : _MOUSE_SCROLL_OUT,
    "HOLD_MOUSE" : _MOUSE_HOLD,
    "HOLD_KEYS" : _KEYBOARD_HOLD,
}


class BadShortcut(Exception):
    """Raised when erroneous shortcut found in file."""
    pass

class Shortcut:
    """A list of EventGroups to execute sequentially."""

    def __init__(self, event_groups, label):
        """Create a Shortcut, given list of event groups and a human-readable label."""
        self.event_groups = event_groups
        self.label = label

    def execute(self, keyboard, mouse, consumer_control):
        """Perform all the event groups in this shortcut."""
        for event_group in self.event_groups:
            event_group.execute(keyboard, mouse, consumer_control)

    @classmethod
    def read_shortcuts(cls, filename):
        """Read all shortcuts from given file."""

        line_re = ure.compile(r'^\s*(\d+)\s+([^;]*);(.*)$')

        shortcut_dict = {}

        input_file = open(filename, 'r')
        for line in input_file:
            # Skip empty or comment lines.
            line = line.strip()
            if not line or line[0] == '#':
                continue

            match = line_re.match(line)
            if not match:
                raise BadShortcut("Bad shortcut line: " + line)

            switch_num = int(match.group(1))
            event_groups = tuple(EventGroup(event_group_str.strip())
                                 for event_group_str in match.group(2).split())
            label = match.group(3).strip()

            # Append the Shortcut to the list of shortcuts for this switch.
            shortcut_dict.setdefault(switch_num, []).append(Shortcut(event_groups, label))

        return shortcut_dict

class EventGroup:
    """A group of keyboard or mouse events to execute simultaneously."""
    def __init__(self, event_group_str):
        event_group_strings = event_group_str.split('-')
        # Convert each event string to an event.
        self.events = tuple(self.str_to_event(event_group_string.strip())
                            for event_group_string in event_group_strings)

    @staticmethod
    def str_to_event(event_str):
        """Parse an event into an integer code."""
        event_str = event_str.upper()
        # Convenience renames of keycodes.
        event_str = _RENAMES.get(event_str, event_str)
        # A Keycode name can be an event.
        keycode = getattr(Keycode, event_str, None)
        if keycode is not None:
            return keycode | _KEYBOARD_EVENT

        # A ConsumerControlCode name can be an event.
        consumer_control_code = getattr(ConsumerControlCode, event_str, None)
        if consumer_control_code is not None:
            return consumer_control_code | _CONSUMER_CONTROL_EVENT

        # Finally, look up unmatched event_str's.
        other_event = _OTHER_EVENTS.get(event_str, None)
        if other_event is not None:
            return other_event

        raise BadShortcut("Unknown event:", event_str)

    def execute(self, keyboard, mouse, consumer_control):
        """Perform the events in this group."""
        keyboard_hold = False
        mouse_hold = False
        # Consolidate key and mouse presses together.
        keycodes = []
        mouse_press = 0
        for event in self.events:
            if event == _KEYBOARD_HOLD:
                keyboard_hold = True
            elif event == _MOUSE_HOLD:
                mouse_hold = True
            elif event == _MOUSE_SCROLL_IN:
                mouse.move(wheel=-1)
            elif event == _MOUSE_SCROLL_OUT:
                mouse.move(wheel=1)
            elif event & _KEYBOARD_EVENT:
                keycodes.append(event & _EVENT_MASK)
            elif event & _MOUSE_EVENT:
                mouse_press |= event & _EVENT_MASK
            elif event &_CONSUMER_CONTROL_EVENT:
                consumer_control.send(event & _EVENT_MASK)

        # Do the keycodes first since it might be shift-left-button, etc.
        if keycodes:
            keyboard.press(*keycodes)
        if mouse_press:
            mouse.press(mouse_press)
        if not mouse_hold:
            mouse.release_all()
        if not keyboard_hold:
            keyboard.release_all()
