# DS1054Z Screen_Capture
'ds1054-capture' is a Python script that captures whatever is displayed on the screen of a Rigol DS1000Z series oscilloscope.

It can save data as an image of the oscilloscope screen, or as a text file in CSV (Comma Separated Values) format.

To achieve this, SCPI (Standard Commands for Programmable Instruments) are sent from the computer
to the oscilloscope, using the LXI (LAN-based eXtensions for Instrumentation) protocol over a Telnet connection.
The computer and the oscilloscope are connected together by a LAN (Local Area Network).

Tested with Linux Ubuntu 18.04, Python 3.6.

User Manual:
-----------
This program captures either the waveform or the whole screen
    of a Rigol DS1000Z series oscilloscope, then save it on the computer
    as a CSV, PNG or BMP file with a timestamp in the file name.

    The program is using LXI protocol, so the computer must have a LAN connection with the oscilloscope.

    If an IP is not specified, the program will poll the ARP table for a Rigol hardware address.

Usage syntax:

    ds1054-capture [png|bmp|csv] [oscilloscope_IP]

Usage examples:

    ds1054-capture
    ds1054-capture csv
    ds1054-capture 192.168.1.3
    ds1054-capture bmp 192.168.1.3