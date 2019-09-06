from threading import Thread
import logging
import time
import sys
import socket
import datetime
import subprocess

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
_init_ = {
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
    'imu' : '',
    'serial' : '',
    'aprs' : aprs,
    'eeprom' : '',
    'init' : '',
    'sys' : '',
    'eps' : eps,
    'iridium' : '',
    'telemetry' : telemetry,
    'gps' : gps,
    'radio_output' : '',
    'time' : '',
    'command_ingest' : '',
    'housekeeping' : '',
    '_init_' : _init_
}

logger = logging.getLogger("CI")


def printArg(list):
    string = ""
    for arg in list:
        string += str(arg) + ","
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
global TX_PORT
global UDP_IP
getTime()
TX_PORT = 5555
#getTime()
#RX_PORT = int(input("UI: Enter RX port number(5550-5559)>>"))
UDP_IP = "127.0.0.1"
#msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#msg_lstn.bind((UDP_IP, RX_PORT))

def listen1():
    ack3 = None
    listen_txt = open('listen.txt', 'w')
    listen_txt.truncate(0)
    listen_txt.close()
    while (1==1):
        #ack, addr = msg_lstn.recvfrom(1024)
        listen_txt = open('listen.txt', 'r')
        ack2 = listen_txt.read()
        listen_txt.close()
        if (ack2 != None and ack2 != ack3):
            print ("RX: ", end="")
            print (ack2)
            #subprocess.call(['curl', '-X', 'POST', '-H', "Content-type: application/json", '--data', '{"text":%s}' % ('"%s"' % ack2), 'https://hooks.slack.com/services/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'])
            ack3 = ack2
            ack2 = None
'''t2 = Thread(target=sendloop, args=())
t2.daemon = True
t2.start()'''

t3 = Thread(target=listen1, args=())
t3.daemon = True
t3.start()

while (1==1):
    getTime()
    print('TJREVERB Groundstation')
    for i in submodules.keys():
        print(i)
    submoduleCheck = 0
    methodCheck = 0
    floatCheck = 0
    argsList =[]
    getTime()
    keyin1 = input('UI: Which submodule?\n') #get the input for submodule
    '''if(keyin1 == "send"):
        msg = "TJaprs_echo,helloH"
        msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_snd.sendto(msg.encode(), (UDP_IP, TX_PORT))
        getTime()
        print ('Message sent')'''
    if (keyin1 in submodules):#make sure that keyin1 is in submodule
        submoduleCheck = 1#if it is in, make check to 1
        while (methodCheck == 0):#keep on going until valid method
            #print(submodules[keyin1])
            print("Methods:")
            for j in submodules[keyin1]:
                print(j, submodules[keyin1][j])
            getTime()
            keyin2 = input('UI: Which method?\n')
            if (keyin2 in submodules[keyin1]):#make sure method is in submodules
                methodCheck = 1#change methodcheck to 1
                print(submodules[keyin1][keyin2])
                for i in range(len(submodules[keyin1][keyin2])):
                    getTime()
                    if(submodules[keyin1][keyin2][i] == "int"):#check if arg type is int
                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        while(arg.isdigit() == False):#keep on going until is digit
                            getTime()
                            arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        argsList.append(int(arg))
                    elif(submodules[keyin1][keyin2][i] == "bool"):
                        getTime()
                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        while (arg!= "True" and arg != "False"):
                            getTime()
                            arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        if(arg == "True"):
                            argsList.append(True)
                        if(arg == "False"):
                            argsList.append(False)
                    elif (submodules[keyin1][keyin2][i] == 'float'):
                        while (floatCheck == 0):
                            try:
                                getTime()
                                argsList.append(float(input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")))
                                floatCheck = 1
                            except:
                                floatCheck = 0

                    else: #assumes string arg
                        getTime()
                        arg = input('UI: Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]) + "\n")
                        argsList.append(arg)
                checksum = generate_checksum('TJ' + keyin2 + ',' + printArg(argsList))
                msg = ('TJ' + keyin2 + ',' + printArg(argsList) + checksum)
                getTime()
                print (msg)
                getTime()
                confirm = input('UI: Is this okay? Type y for yes or n for no\n')
                if (confirm == 'y'):
                    msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    msg_snd.sendto(msg.encode(), (UDP_IP, TX_PORT))
                    transmit_txt = open("transmit.txt","w")
                    transmit_txt.truncate(0)
                    transmit_txt.write(msg)
                    transmit_txt.close()
                    getTime()
                    print ('Message sent')
            else:
                print('Invalid method')
    else:
        print('Invalid submodule')
