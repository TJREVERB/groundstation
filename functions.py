from threading import Thread
import logging
import time
import socket
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class listen_class:
    def __init__(self, listenList):
        self.messageList = listenList
        
    def get_list(self):
        return self.messageList

    def reset_list(self):
        self.messageList = []

    def start_listen(self):
        t1 = Thread(target=self.listen, args=())
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
            if "to SATT4" in str(ack): #checks if message received was the one we just sent
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
    return chr(sum1)

def check_checksum (body: str):
    body2 = body[:-1]
    checksum = generate_checksum(body2)
    if (checksum == body[-1]):
        return True;
    else: 
        return False;

def in_module(module):
    if (module in submodules):
        return True
    return False

def in_method(submod, method):
    if (method in submodules[submod]):
        return True
    return False

def check_int(num):
    return (num.isdigit())

def check_bool(booleanVar):
    if (booleanVar == "True" or booleanVar == "False"):
        return (True)
    return (False)

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

def check_args(module, method, argList):
    argumentlist = submodules[module][method]
    if (len(argumentlist) != len(argList)):
        return (False)
    count = 0
    for i in argumentlist:
        if (i == "int"):
            if (check_int(argList[count]) == False):
                return (False)
            count += 1
        elif (i == "bool"):
            if (check_bool(argList[count]) == False):
                return (False)
            count += 1
        elif (i == "float"):
            if (check_float(argList[count]) == False):
                return (False)
            count += 1
        elif (i == "char"):
            if (check_char(argList[count]) == False):
                return (False)
            count += 1
        else:
            count += 1
    return (True)

def send(module, method, argList):  # ASSUMES EVERYTHING HAS BEEN CHECKED
    checksum = generate_checksum('TJ' + module + ',' + method + ',' + print_arg(argList))
    msg = "TJ" + module + "," + method + "," + print_arg(argList) + checksum
    try:  # Message successfully sent
        msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
        city_ref = db.collection(u'Log').document(u'Send')#
        timestamp = get_time()
        city_ref.update({#
            timestamp : msg,#
        })#
        return True
    except:
        return False
