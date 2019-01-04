# Bench Test Kit

This is a collection of python scripts for extracting status & measurement results from various pieces of test equipment.

Used with Linux Ubuntu 18.04, Python 3.6.

## ds1054-capture

'ds1054-capture' retrieves either the current display or current stored dataset from Rigol DS1000Z-series oscilloscope.

It can save data as an image of the oscilloscope screen, or as a text file in CSV (Comma Separated Values) format.

To achieve this, SCPI (Standard Commands for Programmable Instruments) are sent from the computer
to the oscilloscope, using the LXI (LAN-based eXtensions for Instrumentation) protocol over a Telnet connection.
The computer and the oscilloscope are connected together by a LAN (Local Area Network).

If an IP is not specified, the program will poll the ARP table for a Rigol hardware address.

The retrieved data is saved to a file in the current directory with the filename format *<model number>_%Y-%m-%d_%H:%M:%S.<format extension>*

### Usage:

    ds1054-capture [png|bmp|csv] [oscilloscope_IP]

### Usage examples:

    ds1054-capture
    ds1054-capture csv
    ds1054-capture 192.168.1.3
    ds1054-capture bmp 192.168.1.3

## dm3058-capture

'dm3058-capture' retrieves the current display from a Rigol DM3058 Bench Multimeter as a BMP image file.

The retrieved image file is saved to a file in the current directory with the filename format *DM3058_%Y-%m-%d_%H:%M:%S.bmp*

### Usage:

    dm3058-capture [OPTION].. [device_IP]
      -P    Preview image after capture (open in ristretto)
      -I    Upload to imgur after capture (returns URL)

## e36312a-capture

'e36312a-capture' retrieves the current display from a Keysight E36312A Power Supply as a BMP image file.

The retrieved image file is saved to a file in the current directory with the filename format *E36312A_%Y-%m-%d_%H:%M:%S.bmp*

### Usage:

    e36312a-capture [device_IP]

## leontp-capture

'leontp-capture' retrieves status information from a LeoBodnar LeoNTP server using an NTPv4 mode 7 request. An SNTP query is also attempted and reported.

The retrieved information is printed to the console standard output.

### Usage:

    leontp-capture [device_IP]

## Copying

Licensed under GPL-2.0, see *LICENSE*.

Copyright Phil Crump 2017