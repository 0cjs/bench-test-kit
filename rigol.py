import sys
import requests

RIGOL_OUI = "00:19:af"

def dm3058_screenshot(instrument_ip, output_filename):
    with open(output_filename, "wb") as f:
        response = requests.head("http://%s/DM3058_WebControl.html" % (instrument_ip))
        if response.status_code != 200:
            return None
        response = requests.get("http://%s/pictures/Display.bmp" % (instrument_ip), stream=True)
        if response.status_code != 200:
            return None

        total_length = int(response.headers.get('content-length'))
        f.write(response.content)

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


# first TMC byte is '#'
# second is '0'..'9', and tells how many of the next ASCII chars
#   should be converted into an integer.
#   The integer will be the length of the data stream (in bytes)
# after all the data bytes, the last char is '\n'
def tmc_header_bytes(buff):
    return 2 + int(buff[1:2])


def expected_data_bytes(buff):
    return int(buff[2:tmc_header_bytes(buff)])


def expected_buff_bytes(buff):
    return tmc_header_bytes(buff) + expected_data_bytes(buff) + 1


def get_memory_depth(tn):
    # Define number of horizontal grid divisions for DS1054Z
    h_grid = 12

    # ACQuire:MDEPth
    mdep = command(tn, ":ACQ:MDEP?")

    # if mdep is "AUTO"
    if mdep == "AUTO\n":
        # ACQuire:SRATe
        srate = command(tn, ":ACQ:SRAT?")

        # TIMebase[:MAIN]:SCALe
        scal = command(tn, ":TIM:SCAL?")

        # mdep = h_grid * scal * srate
        mdep = h_grid * float(scal) * float(srate)

    # return mdep
    return int(mdep)
