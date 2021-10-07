# code for send.py; modules need update
import time
import socket
import datetime
aprs = {
    'aprs_echo': ['str'],
}

gps = {
    "get_position_packet": [],
    "get_velocity_packet": [],
    "record_gps": [],
    "getsignlegps": [],
    "send": ["str"],
    "findnth": ["str", "char", "int"]
}
_init_ = {
    'enter_normal_mode': ['str'],
    'enter_low_power_mode': ['str']
}

eps = {
    'pin_on': ['str'],
    'pin_off': ['str'],
    'get_PDM_status': ['str']
}
telemetry = {
    'test': ['str']
}

submodules = {
    'adcs': '',
    'eeprom': '',
    'imu': '',
    'serial': '',
    'aprs': aprs,
    'init': '',
    'sys': '',
    'eps': eps,
    'iridium': '',
    'telemetry': telemetry,
    'gps': gps,
    'radio_output': '',
    'time': '',
    'command_ingest': '',
    'housekeeping': '',
    '_init_': _init_
}


def generate_checksum(body: str):
    """
    Given a message body, generate its checksum
    :param body: The body of the message.
    :return: Generated checksum for the message.
    """
    global sum1
    sum1 = sum([ord(x) for x in body[0:-7]])
    sum1 %= 26
    sum1 += 65
    return chr(sum1)


def in_module(module):
    """
    Checks if module is valid module
    """
    if (module in submodules):
        return True
    return False


def in_method(submod, method):
    """
    Checks if method is in module
    """
    if (method in submodules[submod]):
        return True
    return False


def check_args(module, method, argList):
    """
    Checks if the args given are valid
    Goes through the argList and makes sure the given args match the arg type
    """
    argumentlist = submodules[module][method]
    if (len(argumentlist) != len(argList)):
        return (False)
    count = 0
    for i in argumentlist:
        param = argList[count]
        if (i == "int"):
            try:
                int(param)
            except ValueError:
                return False
        elif (i == "bool"):
            if((param == "True" or param == "False") == False):
                return False
        elif (i == "float"):
            try:
                float(param)
            except ValueError:
                return False
        elif (i == "char"):
            if ((param.isalpha() == True and len(param) <= 1) == False):
                return False
        count += 1
    return (True)


def send(module, method, argList):
    """
    Assumes all methods have been checked and are valid
    Generates messege based on module, method, argList
    Sends the message using sockets
    Assume everything has been checked
    """
    tx_port = 5555
    udp_ip = "127.0.0.1"
    no_checksum_msg = 'TJ:C;' + module + ';' + method + ';'
    for i in range(len(argList)-1):
        no_checksum_msg += str(argList[i]) + ";"
    no_checksum_msg += str(argList[-1])
    #checksum = generate_checksum(no_checksum_msg)
    #msg = no_checksum_msg + checksum
    msg = no_checksum_msg
    try:  # Message successfully sent
        msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
        return True
    except:
        return False
