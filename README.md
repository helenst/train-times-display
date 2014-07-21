Train Times Display
===================

[![Arduino showing next train times](http://farm9.staticflickr.com/8351/8328703591_f028941a37.jpg)](http://www.flickr.com/photos/orangebrompton/8328703591/)

Set of scripts to read in UK train information and displays the next two trains on an LCD character display. It can be run on a Raspberry pi, or on a PC controlling Arduino over serial.

Uses RGB backlight for quick status indication - green for all OK, yellow for minor delays, red for severe delays.


History
-------

I made this because I live near the station and am always rushing out to catch some train or other. The idea is that I will be able to glance at the display while I'm trying to find my keys / tie my shoes and know whether it's worth hurrying.

It started out as an arduino project, with a master python script running on a server and pushing display commands to the Arduino - because (a) I didn't have any arduino networking and (b) I'd rather do parsing / logic stuff in Python than C. It became clear that this would make more sense as a Raspberry Pi script so I bought the right GPIO bits and moved it across.

The Arduino code is still there and can be enabled in the config by changing display mode.


Architecture
------------

The Python script is a long running process which scrapes live departure boards every five minutes and 
updates the display every minute.


### Arduino ###

The driver script runs on a PC, which drives the Arduino over a USB cable. The Arduino acts as a dumb display, receiving and interpreting display commands. The Arduino side knows nothing about trains and could easily be repurposed.


### Raspberry Pi ###

The driver script runs on the Pi, driving the display over the GPIO interface using [Adafruit's char LCD code](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code)


Requirements
------------

### Software ###

* python 3 (I'm using 3.2.3, untested on anything else)
* pyserial (arduino only)
* beautifulsoup v4
* For Arduino, Arduino software >= 1.0.1 
* For Raspberry Pi, extra requirements detailed in the [Adafruit instructions](http://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/necessary-packages).

### Hardware ###

* Arduino (I used Uno) with USB cable. OR:
* Raspberry pi + GPIO breakout kit + network connection
* LCD 16x2 display (possibly RGB)
* 0.1" header, 16 pins long
* Soldering equipment
* Breadboard
* Jumper wires
* 10K potentiometer


Instructions
------------

This is how you wire it up:
[Arduino](http://learn.adafruit.com/character-lcds/wiring-a-character-lcd) / 
[Raspberry Pi](http://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/wiring)

If you are using an RGB LCD, as I am, extra wiring will be needed for the backlights (I only wire in the red and green as this is all I use - happily, this nicely matches the Pi's original 8 GPIO pins). Make sure you are either using an LCD with built in backlight resistors (e.g. the Adafruit boards), or add your own into the circuit

The Arduino code is in LcdSerial/LcdSerial.ino.

You should edit config.py and comment out the relevant DISPLAY line depending on which hardware you are using.

Once all the software requirements are installed, try running it.

    python3 run.py
    
You may need to further edit config.py to get the correct serial device, depending on your system. You might also need to play around with device file permissions.

When it's working, the LCD should start to update with train times every minute. By default it's set up for Haslemere, my home town. You can set up your own local station in the stations directory and tell config.py to use that instead.


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



Thanks
------
* Thanks to adafruit for the [excellent character LCD tutorials](http://learn.adafruit.com/character-lcds/overview)
* Thanks to [dgym](https://github.com/dgym) for helping fix my rusty C.
* Begrudging thanks to NRE for at least putting your live departure info on a fixed, scrapable URL (now, please open it up properly!). Also for providing me with plenty of opportunities to test delay data. ;P
