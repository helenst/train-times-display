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


Commands can be concatenated. e.g.

    'cm\x00\x01wHello\0'


Future work
-----------

* Countdown to next train
* Display next 2 trains in any direction
* Use RGB backlit display and light up red when there are problems


Thanks
------
* Thanks to adafruit for the [excellent character LCD tutorial](http://learn.adafruit.com/character-lcds/overview)
* Thanks to [dgym](https://github.com/dgym) for helping fix my rusty C.

