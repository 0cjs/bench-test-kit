import subprocess

def find_arp(INSTRUMENT_OUI):
    result = subprocess.check_output("arp -n | grep '%s' | awk '{print $1}'" % (INSTRUMENT_OUI), shell=True)
    result_string = result.decode("utf-8").strip()
    if not result_string:
        return None
    return result_string