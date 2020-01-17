from threading import Thread
import logging
import time
# import sys
import socket
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#logging.basicConfig(filename='event_log.log',level=logging.DEBUG)
messageList = []
'''
    SEND MESSAGE:
    in_module
    in_method
    check_args
    send
    '''
# import subprocess
cred = credentials.Certificate("groundstation-listen-log-firebase-adminsdk-h2jfr-9d71ce0bdb.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
tx_port = 5555
udp_ip = "127.0.0.1"

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


def get_time():  # get_time()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return (st)


#def get_logger():
    #return (logging.getLogger("CI"))


def print_arg(list):
    string = ""
    for arg in list:
        string += str(arg) + ","
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
    #logger = get_logger()
    #logger.debug('CHECKOUT :' + chr(sum1) + ";")
    return chr(sum1)


class listen_class:
    def __init__(self, listenList):
        self.messageList = listenList
        # self.messageList.append(messageList)

    def get_list(self):
        return self.messageList

    def reset_list(self):
        self.messageList = []

    def start_listen(self):
        t1 = Thread(target=self.listen_test, args=())
        t1.daemon = True
        t1.start()

    def listen_test(self):  # FOR TESTING
        while True:
            message = input("What is your message?")
            self.messageList.append(message)
            print(self.messageList)

    def listen(self):
        UDP_IP = "127.0.0.1"
        RX_PORT = 5557
        while True:
            msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            msg_lstn.bind((UDP_IP, RX_PORT))
            ack, addr = msg_lstn.recvfrom(1024)
            #print (ack)
            #time.sleep(1)
            #REDUDANCY CHECK
            if "to SATT4" in str(ack):
                # getTime()
                print("RX: ", end="")
                print(ack)
                self.messageList.append(ack)
                timestamp = get_time()
                city_ref = db.collection(u'Log').document(u'Listen')
                city_ref.update({
                    timestamp : ack,
                })
            checksum = generate_checksum(ack)
            time.sleep(1)
            #self.messageList.append(ack)
                # return(str(ack))
            #print ("RX: " + get_time(), end="")
            #print (ack)
            # print(ack)
            # self.messageList.append(ack)
def in_module(module):
    # get_time()
    # submod = input("UI: Which Module?\n")
    # while(submod not in submodules):
    # get_time()
    # submod = input("UI: Which Module?\n")
    # return(submod)
    if (module in submodules):
        return True
    return False


def print_Methods(submodule):
    methods = "<font color=green></br>"
    for i in submodules[submodule].keys():
        print(i)
        methods += i + "</br>"
    methods += "</font>"
    return (methods)


def in_method(submod, method):
    '''method = input("UI: Which method?\n")
        while(method not in submodules[submod]):
        get_time()
        method = input("UI: Which method?\n")
        return(method)'''
    if (method in submodules[submod]):
        return True
    return False


def check_int(num):
    return (num.isdigit())


def check_bool(booleanVar):
    # takes in str
    if (booleanVar == "True" or booleanVar == "False"):
        return (True)
    return (False)


# def send_message()

def check_float(floatVar):
    try:
        float(floatVar)
        return (True)
    except ValueError:
        return (False)


def check_char(charVal):
    if (charVal.isalpha() == True and len(charVal) <= 1):
        return (True)
    return False


def arg_length(module, method):
    return (len(submodules[module][method]))


def get_arg(module, method):
    argStr = "<font color=green></br>Args: ["
    for i in (submodules[module][method]):
        argStr += i + ", "
    argStr += "]<font>"
    return (argStr)


def check_args(module, method, argList):
    argumentlist = submodules[module][method]
    if (len(argumentlist) != len(argList)):
        return (False)
    count = 0
    for i in argumentlist:
        # print(count)
        # print(argList[count])
        if (i == "int"):
            if (check_int(argList[count]) == False):
                # print("int")
                return (False)
            count += 1
        elif (i == "bool"):
            if (check_bool(argList[count]) == False):
                # print("bool")
                return (False)
            count += 1
        elif (i == "float"):
            if (check_float(argList[count]) == False):
                # print("float")
                return (False)
            count += 1
        elif (i == "char"):
            if (check_char(argList[count]) == False):
                # print("char")
                return (False)
            count += 1
        else:
            count += 1
    return (True)


def get_message(module, method, argList):
    checksum = generate_checksum(
        'TJ' + module + ',' + method + ',' + print_arg(argList))
    msg = "TJ" + module + "," + method + "," + print_arg(argList) + checksum
    return (msg)


def send(module, method, argList):  # ASSUMES EVERYTHING HAS BEEN CHECKED
    #logging.debug("log working")
    log = open("event_log.log", "a")
    checksum = generate_checksum(
        'TJ' + module + ',' + method + ',' + print_arg(argList))
    msg = "TJ" + module + "," + method + "," + print_arg(argList) + checksum
    try:  # Message successfully sent
        msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
        #log.write(msg)
        city_ref = db.collection(u'Log').document(u'Send')
        timestamp = get_time()
        city_ref.update({
            timestamp : msg,
        })
        return True
    except:
        log.write("ERROR: MESSAGE FAILED TO SEND. MESSAGE: " + msg)
        return False
# listen_list()
