import subprocess
from os import system
from requests import post
from base64 import b64encode
from json import loads

import socket
from struct import unpack
from time import localtime

def find_arp(INSTRUMENT_OUI):
    with open('/proc/net/arp') as f:
        f.readline()    # Drop header line
        for line in f:
            words = line.split()
            ipaddr_str, hwaddr, = words[0], words[3]
            if hwaddr.startswith(INSTRUMENT_OUI):
                return ipaddr_str
    return None

def instrument_ping(instrument_ip):
    if system("ping -c 1 %s > /dev/null" % (instrument_ip)) == 0:
        return True
    else:
        return False

def image_preview(filename):
    subprocess.Popen(["ristretto", filename])

def imgur_post(filename, title):
    imgur_url = "https://api.imgur.com/3/upload.json"
    imgur_client_id = "304caf5018e5332"
    imgur_headers = { "Authorization": "Client-ID %s" % (imgur_client_id) }
    image_data = b64encode(open(filename, 'rb').read())
    image_req = post(
        imgur_url,
        headers = imgur_headers,
        data = {
            'image': image_data,
            'type': 'base64',
            'name': filename,
            'title': title
        }
    )
    req_data = loads(image_req.text)["data"]
    if image_req.status_code == 200:
        print("Uploaded: %s" % (req_data["link"]))
    else:
        print("Imgur Upload Failed: %s" % (req_data["error"]))

class SNTP_Request:
    pass

def sntp_request(server='0.uk.pool.ntp.org'):
    UNIX_NTP_DELTA = 2208988800

    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b

    addr = socket.getaddrinfo(server, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()

    response = SNTP_Request()

    response.stratum = (unpack("!B", msg[1:2])[0])
    response.ref_id = unpack("4s", msg[12:16])
    response.ts_ref = unpack("!I", msg[16:20])[0]
    response.ts_orig = unpack("!I", msg[24:28])[0]
    response.ts_rx = unpack("!I", msg[32:36])[0]
    response.ts_tx = unpack("!I", msg[40:44])[0]

    if response.stratum == 0:
        # KoD
        return response

    response.time = localtime(response.ts_tx - UNIX_NTP_DELTA)
    response.timestamp = "%d-%02d-%02d %02d:%02d:%02d" % (response.time.tm_year, response.time.tm_mon, response.time.tm_mday, response.time.tm_hour, response.time.tm_min, response.time.tm_sec)

    return response
