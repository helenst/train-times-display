Train Times Display
===================

![Arduino showing next train times](http://farm9.staticflickr.com/8488/8279350628_0b14fb578c.jpg)

This is a little arduino project which reads in UK train information and displays the next trains 
on an LCD character display. I made it because I live near the station and am always rushing out to
catch some train or other. The idea is that I will be able to glance at the display while I'm trying
to find my keys / tie my shoes and know whether it's worth hurrying.


Architecture
------------

Consists of a dumb display Arduino on the end of a USB cable, driven by a Python script which contains most of the logic.

The Arduino knows nothing about train times - it interprets commands from the USB input to perform actions
on the character display using the LiquidCrystal library. It knows nothing about train times and is completely generic - 
you could program the chip once and repurpose it later when you're bored with trains.

The Python script is a long running process which scrapes live departure boards on a regular basis, decides what to display 
and updates the display every minute.


Requirements
------------

### Software ###

* python 3 (I'm using 3.2.3, untested on anything else)
* pyserial
* beautifulsoup v4

### Hardware ###

* Arduino (I used Uno)
* LCD 16x2 display
* 0.1" header, 16 pins long
* Soldering equipment
* Breadboard
* Jumper wires
* 10K potentiometer


Instructions
------------

[This is how you wire it up](http://learn.adafruit.com/character-lcds/wiring-a-character-lcd).

Once all the software requirements are installed, try running it.

    python3 run.py

You may need to edit config.py to get the right serial device, depending on your system. You might also need to 
play around with device file permissions.

When it's working, the LCD should start to update with train times every minute. By default it's set up for Haslemere,
my home town. You can set up your own local station in the stations directory and tell config.py to use that instead.


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
    
means clear the screen, move to the start of the second row and print Hello


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
