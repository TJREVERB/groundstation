from threading import Thread
import logging
import time
import serial
aprs = {
    'aprs_echo' : ['str'],
    'int_function' : ['str', 'int', "bool", "float"]
}

gps = {
    "get_position_packet": [],
    "get_velocity_packet": [],
    "record_gps": [],
    "getsignlegps": [],
    "send": ["str"],
    "findnth": ["str", "char", "int"]
}
__init__ = {
    'enter_normal_mode' : ['str'],
    'enter_low_power_mode' : ['str']
}

eps = {
    'pin_on' : ['str'],
    'pin_off' : ['str'],
    'get_PDM_status' : ['str']
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
    'telemetry.py' : '',
    'aprs.py.save.1' : '',
    'gps.py' : '',
    'radio_output.py' : '',
    'time' : '',
    'command_ingest.py' : '',
    'housekeeping.py' : '',
    'sampletextgps.txt' : '',
    '__init__.py' : __init__
}
serialPort = "/dev/ttyUSB0"
ser = serial.Serial(serialPort, 19200)

logger = logging.getLogger("CI")

sendbuffer = []

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

def sendloop():
    global sendbuffer
    while (True):
        while len(sendbuffer) > 0:  #CHECKS IF THERE IS SOMETHING IN SENDBUFFER
            ser.write(sendbuffer[0].encode("utf-8"))
            #WRITES THE FIRST ELEMENT OF SENDBUFFER
            sendbuffer = sendbuffer[1:]
            #DELETES FIRST ELEMENT OF SENDBUFFER AFTER IT IS SENT
            time.sleep(.01)

#LISTENS FOR ANY COMMUNICATION COMING FROM THE APRS OVER THE SERIAL LINE
def listen():
    while (True):
        # IF I GET SOMETHING OVER THE SERIAL LINE
        zz = ser.inWaiting()
        # READ THAT MANY BYTES
        rr = ser.read(size=zz)
        if zz > 0:
            time.sleep(.5)
            # CHECK AFTER .5 SECONDS, AND READ ANYTHING THAT GOT LEFT BEHIND
            zz = ser.inWaiting()
            rr += ser.read(size=zz)
            print(rr)
            #log('GOT: ' + rr)
            # return (rr)
            # return rr

t2 = Thread(target=sendloop, args=())
t2.daemon = True
t2.start()

t3 = Thread(target=listen, args=())
t3.daemon = True
t3.start()

while (1==1):
    print('TJREVERB Groundstation')
    print(submodules)
    submoduleCheck = 0
    methodCheck = 0
    floatCheck = 0
    argsList =[]
    keyin1 = input('Which submodule?') #get the input for submodule
    if (keyin1 in submodules):#make sure that keyin1 is in submodule
        submoduleCheck = 1#if it is in, make check to 1
        while (methodCheck == 0):#keep on going until valid method
            print(submodules[keyin1])
            keyin2 = input('Which method?')
            if (keyin2 in submodules[keyin1]):#make sure method is in submodules
                methodCheck = 1#change methodcheck to 1
                print(submodules[keyin1][keyin2])
                for i in range(len(submodules[keyin1][keyin2])):
                    if(submodules[keyin1][keyin2][i] == "int"):#check if arg type is int
                        arg = input('Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]))
                        while(arg.isdigit() == False):#keep on going until is digit
                            arg = input('Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]))
                        argsList.append(int(arg))
                    elif(submodules[keyin1][keyin2][i] == "bool"):
                        arg = input('Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]))
                        while (arg!= "True" and arg != "False"):
                            arg = input('Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]))
                        if(arg == "True"):
                            argsList.append(True)
                        else:
                            argsList.append(False)
                    elif (submodules[keyin1][keyin2][i] == 'float'):
                        while (floatCheck == 0):
                            try:
                                argsList.append(float(input('Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]))))
                                floatCheck = 1
                            except:
                                floatCheck = 0

                    else:#assumes string arg
                        arg = input('Which arg for arg type: ' + str(submodules[keyin1][keyin2][i]))
                        argsList.append(arg)
                checksum = generate_checksum('TJ' + keyin2 + '_' + argsList[0])
                print('TJ' + keyin2 + '_'  + printArg(argsList)+checksum)
                sendbuffer.append('TJ' + keyin2 + '_'  + printArg(argsList)+checksum+'\r\n')
            else:
                print('Invalid method')
    else:
        print('Invalid submodule')

