from threading import Thread
import logging
import time
# import sys
import socket
import datetime

# import subprocess

tx_port = 5555
udp_ip = "127.0.0.1"


def get_time():  # get_time()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st, end=" ")


def get_logger():
    return (logging.getLogger("CI"))


def print_arg(list):
    string = ""
    for arg in list:
        string += str(arg) + ", "
    return (string[:-1])


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
    logger = get_logger()
    logger.debug('CHECKOUT :' + chr(sum1) + ";")
    return chr(sum1)


def listen():
    def listen_loop():
        ack3 = None
        listen_txt = open('listen.txt', 'w')
        listen_txt.truncate(0)
        listen_txt.close()
        while (1 == 1):
            # ack, addr = msg_lstn.recvfrom(1024)
            listen_txt = open('listen.txt', 'r')
            ack2 = listen_txt.read()
            listen_txt.close()
            if (ack2 != None and ack2 != ack3):
                print("RX: ", end="")
                print(ack2)
                # subprocess.call(['curl', '-X', 'POST', '-H', "Content-type: application/json", '--data', '{"text":%s}' % ('"%s"' % ack2), 'https://hooks.slack.com/services/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'])
                ack3 = ack2
                ack2 = None

    Thread(target=listen_loop, daemon=True).start()


def send():
    #######################################################

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
        'eeprom': '',
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

    ###################################################
    get_time()
    print("TJREVERB Groundstation")
    # PRINT SUBMODULES METHOD
    submoduleCheck = 0
    methodCheck = 0
    floatCheck = 0
    argsList = []
    keyin1 = input('UI: Which submodule?\n')  # get the input for submodule
    if (keyin1 in submodules):  # make sure that keyin1 is in submodule
        submoduleCheck = 1  # if it is in, make check to 1
        while (methodCheck == 0):  # keep on going until valid method
            # print(submodules[keyin1])
            print("Methods:")
            for j in submodules[keyin1]:
                print(j, submodules[keyin1][j])
            get_time()
            keyin2 = input('UI: Which method?\n')
            if (keyin2 in submodules[keyin1]):  # make sure method is in submodules
                methodCheck = 1  # change methodcheck to 1
                print(submodules[keyin1][keyin2])
                for i in range(len(submodules[keyin1][keyin2])):
                    get_time()
                    if (submodules[keyin1][keyin2][i] == "int"):  # check if arg type is int
                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        while (arg.isdigit() == False):  # keep on going until is digit
                            get_time()
                            arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        argsList.append(int(arg))
                    elif (submodules[keyin1][keyin2][i] == "bool"):
                        get_time()
                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        while (arg != "True" and arg != "False"):
                            get_time()
                            arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        if (arg == "True"):
                            argsList.append(True)
                        if (arg == "False"):
                            argsList.append(False)
                    elif (submodules[keyin1][keyin2][i] == 'float'):
                        while (floatCheck == 0):
                            try:
                                get_time()
                                argsList.append(float(
                                    input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")))
                                floatCheck = 1
                            except:
                                floatCheck = 0

                    else:  # assumes string arg
                        get_time()
                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        argsList.append(arg)
                checksum = generate_checksum('TJ' + keyin2 + ',' + print_arg(argsList))
                msg = ('TJ' + keyin2 + ',' + print_arg(argsList) + checksum)
                get_time()
                print(msg)
                get_time()
                confirm = input('UI: Is this okay? Type y for yes or n for no\n')
                if (confirm == 'y'):
                    msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
                    transmit_txt = open("transmit.txt", "w")
                    transmit_txt.truncate(0)
                    transmit_txt.write(msg)
                    transmit_txt.close()
                    get_time()
                    print('Message sent')
            else:
                print('Invalid method')
    else:
        print('Invalid submodule')
