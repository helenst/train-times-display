Train Times Display
===================

![Arduino showing next train times](http://farm9.staticflickr.com/8488/8279350628_0b14fb578c.jpg)

This is a little arduino project which aims to display the next train times on a 16x2 LCD display,
because I live near the station and always like to know how long I've got / how much I need to panic
when getting ready to go out. Hopefully one day it will sit in the hallway and be extremely useful.


Arduino
-------

Acts as a dumb display, interpreting commands from the USB input to perform actions
on the 16x2 LCD display using the LiquidCrystal library.

Uses the built in Serial library to read a simple display protocol from the USB port


Python Script
-------------

The brains of the operation - scrapes live departure boards for the station in question,
decides what to display and sends commands over the serial port

Requirements
------------
### Software ###

* python 3
* pyserial
* beautifulsoup v4

### Hardware ###

* Arduino
* LCD 16x display + header so it sticks into the breadboard
* Breadboard, jumper wires, potentiometer


Protocol
--------

Arduino sends a single zero when it's ready for action. (This is because it resets
itself on new serial connection - we don't want to throw commands at it until it's ready)

Commands consist of a single letter followed by the arguments for that command

MOVE (m)

Move cursor to specified column and row

e.g. 'm\x00\x01' moves cursor to col 0 row 1


WRITE (w)

Write string at current cursor position
Must be null terminated.

e.g. 'wHello\0'


CLEAR (c)

Clear screen

e.g. 'c'


SCROLL LEFT (l)

Scroll the display left by the specified number of columns

e.g. 'l\x05' scrolls left by 5


SCROLL RIGHT (r)

Scroll the display right by the specified number of columns

e.g. 'r\x05' scrolls right by 5


Commands can be concatenated. e.g.

    'cm\x00\x01wHello\0'


Future work
-----------

* Use RGB backlit display and light up red when there are problems
* Quite possibly make a Raspberry Pi version


Thanks
------
* Thanks to adafruit for the [excellent character LCD tutorial](http://learn.adafruit.com/character-lcds/overview)
* Thanks to [dgym](https://github.com/dgym) for helping fix my rusty C.
* Begrudging thanks to NRE for at least putting your live departure info on a fixed, scrapable URL (now, please open it up properly!). Also for providing me with plenty of opportunities to test delay data. ;P
