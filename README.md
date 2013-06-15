Train Times Display
===================

[![Arduino showing next train times](http://farm9.staticflickr.com/8351/8328703591_f028941a37.jpg)](http://www.flickr.com/photos/orangebrompton/8328703591/)

This is a little project which reads in UK train information and displays the next trains 
on an LCD character display. I made it because I live near the station and am always rushing out to
catch some train or other. The idea is that I will be able to glance at the display while I'm trying
to find my keys / tie my shoes and know whether it's worth hurrying.

It works with either Arduino or Raspberry Pi, depending on which display mode is chosen.


Architecture
------------

### Arduino ###

The Python script runs on a PC, which drives the Arduino over a USB cable. The Arduino acts as a dumb display, receiving 
and interpreting display commands from the driver script. It knows nothing about trains and could easily be repurposed.


### Raspberry Pi ###

The Python script runs on the Pi, driving the display over the GPIO interface using [Adafruit's char LCD code](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code)


The script is a long running process which scrapes live departure boards every five minutes and updates the display every minute.


Requirements
------------

### Software ###

* python 3 (I'm using 3.2.3, untested on anything else)
* pyserial
* beautifulsoup v4
* If you are using Arduino, Arduino software >= 1.0.1 
* If you are using Raspberry pi, extra requirements detailed in the [Adafruit instructions](http://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/necessary-packages).

### Hardware ###

* Arduino (I used Uno) with USB cable. OR:
* Raspberry pi + GPIO breakout kit + network connection
* LCD 16x2 display
* 0.1" header, 16 pins long
* Soldering equipment
* Breadboard
* Jumper wires
* 10K potentiometer


Instructions
------------

[This is how you wire it up](http://learn.adafruit.com/character-lcds/wiring-a-character-lcd).

The Arduino code is in LcdSerial/LcdSerial.ino.

You should edit config.py and comment out the relevant DISPLAY line depending on which hardware you are using.

Once all the software requirements are installed, try running it.

    python3 run.py
    
You may need to further edit config.py to get the correct serial device, depending on your system. You might also need to 
play around with device file permissions.

When it's working, the LCD should start to update with train times every minute. By default it's set up for Haslemere,
my home town. You can set up your own local station in the stations directory and tell config.py to use that instead.


Serial Display Protocol (Arduino only)
--------------------------------------

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
* Try the capacitor solution for reset-on-serial


Thanks
------
* Thanks to adafruit for the [excellent character LCD tutorials](http://learn.adafruit.com/character-lcds/overview)
* Thanks to [dgym](https://github.com/dgym) for helping fix my rusty C.
* Begrudging thanks to NRE for at least putting your live departure info on a fixed, scrapable URL (now, please open it up properly!). Also for providing me with plenty of opportunities to test delay data. ;P
