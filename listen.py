import socket
import time
import datetime

def listen():
    UDP_IP = "127.0.0.1"
    RX_PORT = 5557

    global ack
    global ack2
    ack = None
    ack2 = None

    def getTime():
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(st, end =" ")

    def lastTransmission():
        global ack2
        transmit_txt = open('transmit.txt', 'r')
        ack2 = transmit_txt.read()
        transmit_txt.close()

    def generate_checksum(body: str):
        global sum1
        sum1 = sum([ord(x) for x in body[0:-7]])
        sum1 %= 26
        sum1 += 65
        #logger.debug('CHECKOUT :' + chr(sum1) + ";")
        return chr(sum1)

    msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    msg_lstn.bind((UDP_IP, RX_PORT))

    print ('LISTEN')
    while (1==1):
        ack, addr = msg_lstn.recvfrom(1024)
        print (ack)
        time.sleep(1)
        lastTransmission()
        #if redundancyCheck() == False:
        if "to SATT4" in str(ack):
            getTime()
            print ("RX: ", end="")
            print (ack)
            listen_txt = open("listen.txt","w")
            listen_txt.truncate(0)
            listen_txt.write(str(ack))
            listen_txt.close()
            ack = None

