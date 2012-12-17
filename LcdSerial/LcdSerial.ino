#include <stdarg.h>

/*

  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Based on the following tu:
 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

#include <LiquidCrystal.h>

// Set up the data pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup()
{
    // Set up the serial port connection
    Serial.begin(9600);
    Serial.flush();

    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2);
}


// Read bytes from serial port into buffer
// Return number of bytes read

int readSerialData(char* buffer, int bufsize)
{
    int i = 0;

    if (Serial.available())
    {
        while (Serial.available() && i < (bufsize-1))
        {
            buffer[i++] = Serial.read();
        }
    }

    return i;
}


/*
 * Interpret and run the next command in the buffer
 *
 * @return number of characters consumed,
 *  or -1 if no valid command recognised
 *
 * Returns zero if nothing was processed - for example
 * if the buffer was not ready, or not enough data was
 * found to supply all of a command's expected arguments
 */
int runCommand(const char* buffer, int len)
{
    if (len < 1)
        return 0;

    switch (buffer[0])
    {
        /*
         * CLEAR
         * Clear the screen - no arguments
         */
        case 'c':
        {
            lcd.clear();
            return 1;
        }

        /*
         * WRITE
         * Write string to screen at current position.
         * Next bytes specify the string until null char is found
         * Example (writes Hello to the screen):
         *      wHello
         */
        case 'w':
        {
            int count = strnlen(++buffer, len-1);
            if (count != len-1)
            {
                lcd.print(buffer);
                return count + 2;
            }
            return 0;
        }

        /*
         * MOVE
         * Move cursor position
         * Next two bytes specify the column and row
         *      m<col><row>
         */
        case 'm':
        {
            if (len >= 3)
            {
                lcd.setCursor(buffer[1], buffer[2]);
                return 3;
            }
            return 0;
        }

        /*
         * SCROLL LEFT
         * Scroll cursor left
         * Next byte specifies number of columns to scroll
         */
        case 'l':
        {
            if (len >= 2)
            {
                for (int i=0; i < buffer[1]; i++) {
                    lcd.scrollDisplayLeft();
                    delay(150);
                }
                return 2;
            }
            return 0;
        }

        /*
         * SCROLL RIGHT
         * Scroll cursor right
         * Next byte specifies number of columns to scroll
         */
        case 'r':
        {
            if (len >= 2)
            {
                for (int i=0; i < buffer[1]; i++) {
                    lcd.scrollDisplayRight();
                    delay(150);
                }
                return 2;
            }
            return 0;
        }
    }

    return -1;
}


/*
 * Serial protocol consists of single character command code
 * followed by arguments for that command
 *
 * Commands can be concatenated:
 * e.g. to clear the screen and write Hello on the bottom line:
 *
 * >>> s.write('cm\x00\x01wHello\0')
 *
 * Commands also may arrive in a fragmented state - the buffer reader takes care of this.
 */

#define BUF_SIZE 256
char buffer[BUF_SIZE];
int buf_len = 0;

void loop()
{
    // Read new chunk into the buffer
    int bytes_read = readSerialData(buffer+buf_len, BUF_SIZE-buf_len-1);
    buf_len += bytes_read;
    int start = 0;

    // Process all complete commands found in the buffer
    while (buf_len > 0)
    {
        int processed = runCommand(buffer+start, buf_len-start);
        if (processed > 0)
        {
            start += processed;
        }
        else if (processed < 0)
        {
            buf_len = 0;
            return;
        }
        else
        {
            break;
        }
    }

    // Reset buffer to new start position
    // (this moves the buffer backwards in memory to overwrite used-up commands
    // and start the next loop iteration from the original position)
    if (start)
    {
        memmove(buffer, buffer+start, buf_len-start);
        buf_len -= start;
    }
}
