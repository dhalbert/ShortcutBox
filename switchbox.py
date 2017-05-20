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

