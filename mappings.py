# switchbox: map switches to mouse and keyboard events
# https://github.com/dhalbert/switchbox
# MIT License: http://www.opensource.org/licenses/mit-license.php
# Copyright 2017 by Daniel C. Halbert
#
# mappings.py:
# Read mappings.py and convert to internal format.

from micropython import const

# A page entry numbers the page and gives it a label to show on the display.
# page-3 "label"
# Switch entries are similar but add one or more key/mouse combinations, done in sequence.
# switch-2 "label" ctrl-x ctrl-y

class Page:
    """A page of switch mappings. Knows its page number."""
    def __init__(self, page_num, label):
        self.page_num = page_num
        self.label = label
        self.switches = []

    def desc(self):
        return 'P{} {}'.format(switch_num, label)


class Switch:
    """A mapping of a particular switch to a sequence of event groups.
    An event is a single keypress or mouse click.
    A Keypress is represented an an int, its keycode.
    Mouse events are represented by functions of zero args which are called to do the work.
    """
    def __init__(self, switch_num, label, events):
        self.switch_num = switch_num
        self.label = label
        self.events = events

    def desc(self):
        return '{}:{}'.format(switch_num, label)


class BadMapping(Exception):
    pass

class Mappings:
    """Read in mappings and organize them."""
    # ex: page-3 "label"
    # PAGE_RE = ure.compile(r'^page-(\d+)\s+"([^"])"\s*$')
    # ex: switch-2 "label" ctrl-x leftclick
    # _SWITCH_RE = ure.compile(r'^switch-(\d+)\s+"([^"])"\s*(.*)$')
    # ure not included by default, so doing ad hoc parsing below.

    def __init__(self, filename):
        """Read all mappings from given file."""
        self.pages = []
        switches_read = []
        f = open(filename, 'r')
        for line in f:
            # Skip empty or comment lines.
            line = line.strip()
            if not line or line[0] == '#':
                continue

            # Extract label.
            try:
                first_quote = line.index('"')
                last_quote = line.rindex('"')
                if first_quote == last_quote:
                    raise BadMapping(line)
                label = line[first_quote + 1 : last_quote]
                rest = line[:first_quote] + line[last_quote + 1:]
            except (ValueError, IndexError):
                raise BadMapping(line)
                
            rest_split = rest.split(None, 1)
            if len(rest_split) == 0:
                raise BadMapping(line)
            cmd_parts = rest_split[0].split('-')
            if len(cmd_parts) != 2:
                raise BadMapping(line)
            cmd_type = cmd_parts[0]
            try:
                cmd_num = int(cmd_parts[1])
            except ValueError:
                raise BadMapping(line)
                
            # Is this a page definition?
            if cmd_type == 'page':
                if self.pages:
                    # Add collected switch definitions to previous page.
                    switches_read.sort(key=lambda switch: switch.switch_num)
                    self.pages[-1].switches =  switches_read
                # Start a new page with its number and label, and an empty list of switches.
                self.pages.append(Page(cmd_num, label))
                switches_read = []
                continue
            
            # Is this a switch definition?
            if cmd_type == 'switch':
                if not self.pages:
                    # Oops, too early. No page to put this switch on.
                    raise ValueError("switch line given before any page")
                if len(rest_split) < 2:
                    raise BadMapping(line)
                switches_read.append(Switch(cmd_num, label, rest_split[1]))

        # At this point, entire file has been read.
        if (not self.pages):
            raise ValueError(filename + "contains no mappings")

        # Add last set of switches to last page.
        switches_read.sort(key=lambda switch: switch.switch_num)
        self.pages[-1].switches = switches_read

        # Sort pages by number now that we have them all.
        self.pages.sort(key=lambda page: page.page_num)


    def print(self, display, page_num):
        """Display info about given page: page number, its labels, and all the switch numbers and
        their labels.
        """
        display.clear()
        page = self.pages[page_num]
        display.print(page.desc())
        display.print("  ")
        for switch in page.switches.values():
            display.print(switch.desc())
            display.print(" ")


    def parse_events(self, events_string):
        """Parse the list of whitespace-separated keyboard and mouse events.
        ex: "shift-ctrl-x leftclick leftclick"
        """
        events = []
        for event_group_string in events_string.split():
            event_group = []
            for event_name in event_group_string.split('-'):
                try:
                    event_group.append(EVENT_NAME[event_string])
                except KeyError:
                    raise KeyError("bad event: " + event_name)
            events.append(event_group)
        return events
