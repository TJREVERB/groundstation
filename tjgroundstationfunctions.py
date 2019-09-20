from threading import Thread
import logging
import time
# import sys
import socket
import datetime
'''
SEND MESSAGE:
in_module
in_method
check_args
send
'''
# import subprocess

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
    print(st, end=" ")


def get_logger():
    return (logging.getLogger("CI"))


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
    logger = get_logger()
    logger.debug('CHECKOUT :' + chr(sum1) + ";")
    return chr(sum1)


def listen():
    #def listen_loop():
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

Thread(target=listen, daemon=True).start()

def in_module(module):
    #get_time()
    #submod = input("UI: Which Module?\n")
    #while(submod not in submodules):
    #get_time()
    #submod = input("UI: Which Module?\n")
    #return(submod)
    if(module in submodules):
        return True
    return False

def print_Methods(submodule):
    print("Methods: ")
    for i in submodules[submodule]:
        print(i)

def in_method(submod, method):
    '''method = input("UI: Which method?\n")
        while(method not in submodules[submod]):
        get_time()
        method = input("UI: Which method?\n")
        return(method)'''
    if(method in submodules[submod]):
        return True
    return False

def check_int(num):
    return(num.isdigit())

def check_bool(booleanVar):
    #takes in str
    if(booleanVar == "True" or booleanVar == "False"):
        return(True)
    return(False)
#def send_message()

def check_float(floatVar):
    try:
        float(floatVar)
        return(True)
    except ValueError:
        return(False)

def check_char(charVal):
    if(charVal.isalpha() == True and len(charVal) <=1):
        return(True)
    return False

def arg_length(module, method):
    return(len(submodules[module][method]))

def check_args(module, method, argList):
    argumentlist = submodules[module][method]
    if(len(argumentlist) != len(argList)):
        return(False)
    count = 0
    for i in argumentlist:
        #print(count)
        #print(argList[count])
        if(i == "int"):
            if(check_int(argList[count]) == False):
                #print("int")
                return(False)
            count += 1
        elif(i == "bool"):
            if(check_bool(argList[count]) == False):
                #print("bool")
                return(False)
            count += 1
        elif(i == "float"):
            if(check_float(argList[count]) == False):
                #print("float")
                return(False)
            count += 1
        elif(i == "char"):
            if(check_char(argList[count]) == False):
                #print("char")
                return(False)
            count += 1
        else:
            count += 1
    return(True)

def send(module, method, argList):#ASSUMES EVERYTHING HAS BEEN CHECKED
    checksum = generate_checksum('TJ' + module + ',' + method + ',' + print_arg(argList))
    msg = "TJ" + module + "," + method + "," + print_arg(argList) + checksum
    msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
    print(msg, "Message sent")
#def send():
#print("hi")
# get_time()
# print("TJREVERB Groundstation")
# # PRINT SUBMODULES METHOD
# #submoduleCheck = 0
# #methodCheck = 0
# floatCheck = 0
# argsList = []
# #keyin1 = in_module()
# #if (keyin1 in submodules):  # make sure that keyin1 is in submodule
# #submoduleCheck = 1  # if it is in, make check to 1
# #while (methodCheck == 0):  # keep on going until valid method
#     # print(submodules[keyin1])
# print_Methods(keyin1)
# get_time()
#     #keyin2 = input('UI: Which method?\n')
# keyin2 = in_method(keyin1)
#     #if (keyin2 in submodules[keyin1]):  # make sure method is in submodules
#         #methodCheck = 1  # change methodcheck to 1
# print(submodules[keyin1][keyin2])
# for i in range(len(submodules[keyin1][keyin2])):
#     #get_time()
#     if (submodules[keyin1][keyin2][i] == "int"):  # check if arg type is int
#         arg = check_int(keyin1, keyin2)
#         argsList.append(arg)
#     elif (submodules[keyin1][keyin2][i] == "bool"):
#         arg = check_bool(keyin1, keyin2)
#         argsList.append(arg)
#     elif (submodules[keyin1][keyin2][i] == 'float'):
#         while (floatCheck == 0):
#             try:
#                 get_time()
#                 argsList.append(float(
#                         input("UI: Which arg for arg type: float\n")))
#                 floatCheck = 1
#             except:
#                 floatCheck = 0
#     elif(submodules[keyin1][keyin2][i] == 'char'):
#         get_time
#         arg = input("UI: Which arg for arg type: char\n")
#         while(arg.isalpha() == False or len(arg) >1):
#             arg = input("UI: Which arg for arg type: char\n")
#         argsList.append(arg)
#     else:  # assumes string arg
#         get_time()
#         arg = input("UI: Which arg for arg type: string\n")
#         argsList.append(arg)
# checksum = generate_checksum('TJ' + keyin2 + ',' + print_arg(argsList))
# msg = ('TJ' + keyin2 + ',' + print_arg(argsList) + checksum)
# get_time()
# print(msg)
# get_time()
# confirm = input('UI: Is this okay? Type y for yes or n for no\n')
# if (confirm == 'y'):
#     msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     msg_snd.sendto(msg.encode(), (udp_ip, tx_port))
#     #transmit_txt = open("transmit.txt", "w")
#     #transmit_txt.truncate(0)
#     #transmit_txt.write(msg)
#     #transmit_txt.close()
#     get_time()
#     print('Message sent')
# '''else:
#     print('Invalid method')
# else:
#     print('Invalid submodule')'''