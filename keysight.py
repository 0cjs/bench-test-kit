import sys
import requests

KEYSIGHT_OUI = "80:09:02"

def e36312a_screenshot(instrument_ip, output_filename):
    with open(output_filename, "wb") as f:
        response = requests.get("http://%s/get/screenshot.bmp" % (instrument_ip), stream=True)
        if response.status_code != 200:
            return None
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s] %3.1f / %3.1fKB" % ('=' * done, ' ' * (50-done), dl/1024.0, total_length/1024.0) )    
                sys.stdout.flush()
        sys.stdout.write("\n") 

    return total_length

def command(tn, scpi):
    answer_wait_s = 1
    response = ""
    while response != b"1\n":
        tn.write("*OPC?\n")  # previous operation(s) has completed ?
        response = tn.read_until(b"\n", 1)  # wait max 1s for an answer

    tn.write(scpi + "\n")
    response = tn.read_until(b"\n", answer_wait_s)
    return response
