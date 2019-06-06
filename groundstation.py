from threading import Thread
import logging
import time
#import serial
import sys
import socket
import datetime

def getTime():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st, end =" ")

aprs = {
    'aprs_echo' : ['str'],
}

gps = {
    "get_position_packet": [],
    "get_velocity_packet": [],
    "record_gps": [],
    "getsignlegps": [],
    "send": ["str"],
    "findnth": ["str", "char", "int"]
}
init = {
    'enter_normal_mode' : ['str'],
    'enter_low_power_mode' : ['str']
}

eps = {
    'pin_on' : ['str'],
    'pin_off' : ['str'],
    'get_PDM_status' : ['str']
}
telemetry = {
    'test' : ['str']
}
submodules = {
    'adcs' : '',
    'eeprom' : '',
    'imu.py' : '',
    'serial' : '',
    'aprs.py' : aprs,
    'eeprom.py' : '',
    'init.py' : '',
    'sys' : '',
    'aprs.py.save' : '',
    'eps.py' : eps,
    'iridium.py' : '',
    'telemetry.py' : telemetry,
    'aprs.py.save.1' : '',
    'gps.py' : gps,
    'radio_output.py' : '',
    'time' : '',
    'command_ingest.py' : '',
    'housekeeping.py' : '',
    'sampletextgps.txt' : '',
    'init.py' : init
}

logger = logging.getLogger("CI")

#sendbuffer = []

def printArg(list):
    string = ""
    for arg in list:
        string += str(arg) + "_"
    return(string[:-1])

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
    logger.debug('CHECKOUT :' + chr(sum1) + ";")
    return chr(sum1)

def ports():
    global TX_PORT
    global RX_PORT
    global UDP_IP
    getTime()
    TX_PORT = int(input("UI: Enter TX port number(5500-5599)>>"))
    getTime()
    RX_PORT = int(input("UI: Enter RX port number(5550-5559)>>"))
    UDP_IP = "127.0.0.1"
    msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    msg_lstn.bind((UDP_IP, RX_PORT))

def listen():
    while (1==1):
        ack, addr = msg_lstn.recvfrom(1024)
        if ack != None:
            print("RX: ", end="")
            print (ack)
            ack = None
#t2 = Thread(target=sendloop, args=())
#t2.daemon = True
#t2.start()
#
#t3 = Thread(target=listen, args=())
#t3.daemon = True
#t3.start()

def check_module(submodule):
    if (submodule in submodules):#make sure that keyin1 is in submodule
        return (True)

def check_method(submodule, method):
    if (method in submodules[submodule]):#make sure method is in
        return (True)

def check_int(arg):
    if(arg.isdigit()):
        return (True)

def check_bool(arg):
    if(arg == "True" or arg == "False" or arg == "true" or arg == "false"):
        return (True)

def check_float(arg):
    try:
        float(arg)
        return (True)
    
    except:
        return (False)

def send(method, argslist, TX_PORT):
    UDP_IP = "127.0.0.1"
    checksum = generate_checksum('TJ' + keyin2 + '_' + printArg(argsList))
    msg = ('TJ' + method + '_'  + printArg(argsList) + checksum)
    msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg_snd.sendto(msg.encode(), (UDP_IP, TX_PORT))



#while (1==1):
#    getTime()
#    print('TJREVERB Groundstation')
#    #print(submodules)
#    for i in submodules.keys():
#        print(i)
#    submoduleCheck = 0
#    methodCheck = 0
#    floatCheck = 0
#    argsList =[]
#    getTime()
#    keyin1 = input('UI: Which submodule?\n') #get the input for submodule
#    if (keyin1 in submodules):#make sure that keyin1 is in submodule
#        submoduleCheck = 1#if it is in, make check to 1
#        while (methodCheck == 0):#keep on going until valid method
#            #print(submodules[keyin1])
#            print("Methods:")
#            for j in submodules[keyin1]:
#                print(j, submodules[keyin1][j])
#            getTime()
#            keyin2 = input('UI: Which method?\n')
#            if (keyin2 in submodules[keyin1]):#make sure method is in submodules
#                methodCheck = 1#change methodcheck to 1
#                print(submodules[keyin1][keyin2])
#                for i in range(len(submodules[keyin1][keyin2])):
#                    getTime()
#                    if(submodules[keyin1][keyin2][i] == "int"):#check if arg type is int
#                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
#                        while(arg.isdigit() == False):#keep on going until is digit
#                            getTime()
#                            arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
#                        argsList.append(int(arg))
#                    elif(submodules[keyin1][keyin2][i] == "bool"):
#                        getTime()
#                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
#                        while (arg!= "True" and arg != "False"):
#                            getTime()
#                            arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
#                        if(arg == "True"):
#                            argsList.append(True)
#                        if(arg == "False"):
#                            argsList.append(False)
#                    elif (submodules[keyin1][keyin2][i] == 'float'):
#                        while (floatCheck == 0):
#                            try:
#                                getTime()
#                                argsList.append(float(input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")))
#                                floatCheck = 1
#                            except:
#                                floatCheck = 0
#
#                    else: #assumes string arg
#                        getTime()
#                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
#                        argsList.append(arg)
#                checksum = generate_checksum('TJ' + keyin2 + '_' + printArg(argsList))
#                msg = ('TJ' + keyin2 + '_'  + printArg(argsList)+checksum)
#                getTime()
#                print (msg)
#                getTime()
#                confirm = input('UI: Is this okay? Type y for yes or n for no\n')
#                if (confirm == 'y'):
#                    msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#                    msg_snd.sendto(msg.encode(), (UDP_IP, TX_PORT))
#                    getTime()
#                    print ('Message sent')
#            else:
#                print('Invalid method')
#    else:
#        print('Invalid submodule')
