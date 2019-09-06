import socket
import time
import datetime

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

#def redundancyCheck():
#    global ack
#    global ack2
#    global decodedMessage
#    decodedMessage = ""
#    ack = str(ack)
#    ack2 = str(ack2)
#    runs = 0
#    runs2 = 0
#    check1 = False
#    while runs <= len(ack):
#        if ack[runs] == ack2[0]:
#            runs3 = runs
#            while ack[runs3] == ack2[runs2]:
#                decodedMessage = decodedMessage + ack[runs3]
#                runs3 = runs3 + 1
#                runs2 = runs2 + 1
#                try:
#                    if ack[runs3] == ack2[runs2]:
#                        pass
#                except:
#                    break
#            checksum = generate_checksum(decodedMessage)
#            if checksum == decodedMessage[runs2 - 1]:
#                break
#            else:
#                runs2 = 0
#        runs = runs + 1
#        try:
#            if ack[runs] == ack2[0]:
#                pass
#       except:
#            break
#    return check1

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

