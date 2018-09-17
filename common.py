import subprocess
from os import system
from requests import post
from base64 import b64encode
from json import loads

def find_arp(INSTRUMENT_OUI):
    result = subprocess.check_output("arp -n | grep '%s' | awk '{print $1}'" % (INSTRUMENT_OUI), shell=True)
    result_string = result.decode("utf-8").strip()
    if not result_string:
        return None
    return result_string

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
