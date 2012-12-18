Train Times Display


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
* python 3
* pyserial
* beautifulsoup v4


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
Thanks to @dgym for helping out with the C.
