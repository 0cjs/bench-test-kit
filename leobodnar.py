# Original version (c) Leo Bodnar 2016

import socket
import struct
from time import gmtime 

LEOBODNAR_OUI = "70:b3:d5"

class LeoNTP_Stats:
    pass

def leontp_stats(instrument_ip):
    VERSION = 4 # NTP version in request
    MODE = 7    # mode 7, private

    PACKETDATA = bytearray(8)   # current request length is 8 bytes, response is 48 bytes

    PACKETDATA[0] = VERSION << 3 | MODE
    PACKETDATA[1] = 0       # sequence
    PACKETDATA[2] = 0x10    # implementation == 0x10, custom
    PACKETDATA[3] = 1       # request code, just 1 for now

    PACKETDATA[4] = 0       # unused for now
    PACKETDATA[5] = 0
    PACKETDATA[6] = 0
    PACKETDATA[7] = 0

    # reference time (in seconds since 1900-01-01 00:00:00) for conversion from NTP time to system time
    TIME1970 = 2208988800

    # Create a UDP socket
    server_address = (instrument_ip, 123)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.5)

    # Send request
    sent = sock.sendto(PACKETDATA, server_address)

    # Receive response
    RX_PACKET, server = sock.recvfrom(1024)

    response = LeoNTP_Stats()

    response.ref_ts0     =(struct.unpack('<I',RX_PACKET[16:20])[0]) / 4294967296.0   # fractional part of the NTP timestamp
    response.ref_ts1     = struct.unpack('<I',RX_PACKET[20:24])[0]   # full seconds of NTP timestamp
    response.uptime      = struct.unpack('<I',RX_PACKET[24:28])[0]
    response.NTP_served  = struct.unpack('<I',RX_PACKET[28:32])[0]
    response.CMD_served  = struct.unpack('<I',RX_PACKET[32:36])[0] # Mode 6 Commands
    response.lock_time   = struct.unpack('<I',RX_PACKET[36:40])[0]
    response.flags       = RX_PACKET[40]
    response.numSV       = RX_PACKET[41]
    response.ser_num     = struct.unpack('<H',RX_PACKET[42:44])[0]   
    response.FW_ver      = struct.unpack('<I',RX_PACKET[44:48])[0]

    sock.close()

    response.time = gmtime(response.ref_ts1 - TIME1970)
    response.timestamp = "%d-%02d-%02d %02d:%02d:%02d.%03d" % (response.time.tm_year, response.time.tm_mon, response.time.tm_mday, response.time.tm_hour, response.time.tm_min, response.time.tm_sec, round(response.ref_ts0*1000))

    return response
