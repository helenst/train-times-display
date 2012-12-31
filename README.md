Train Times Display
===================

![Arduino showing next train times](http://farm9.staticflickr.com/8488/8279350628_0b14fb578c.jpg)

This is a little arduino project which reads in UK train information and displays the next trains 
on an LCD character display. I made it because I live near the station and am always rushing out to
catch some train or other. The idea is that I will be able to glance at the display while I'm trying
to find my keys / tie my shoes and know whether it's worth hurrying.


Arduino
-------

Acts as a dumb display, interpreting commands from the USB input to perform actions
on the character display using the LiquidCrystal library.

It uses the built in Serial library to read a simple display protocol from the USB port


Python Script
-------------

The brains of the operation.

A long running process which scrapes live departure boards on a regular basis, decides what to display 
and updates the display every minute.


Requirements
------------
### Software ###

* python 3
* pyserial
* beautifulsoup v4

### Hardware ###

* Arduino (I used Uno)
* LCD 16x2 display
* 0.1" header, 16 pins long
* Soldering equipment
* Breadboard
* Jumper wires
* Potentiometer


Display Protocol
----------------

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
* Try the capacitor solution for reset-on-serial


Thanks
------
* Thanks to adafruit for the [excellent character LCD tutorial](http://learn.adafruit.com/character-lcds/overview)
* Thanks to [dgym](https://github.com/dgym) for helping fix my rusty C.
* Begrudging thanks to NRE for at least putting your live departure info on a fixed, scrapable URL (now, please open it up properly!). Also for providing me with plenty of opportunities to test delay data. ;P
