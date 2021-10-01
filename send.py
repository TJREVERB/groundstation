import socket


def send(msg: str) -> bool:
    msg+=";" #TEMPORARY FIX TO ACCOUNT FOR GROUNDSTATION BUG: groundstation truncates last character of each message before sending
    if not "TJ;" in msg:
        msg = "TJ;"+msg
    """
    Takes in the message to be sent from the gs
    returns a boolean for whether the message was sent 
    """
    TX_PORT = 5555
    UDP_ID = "127.0.0.1"
    try:  # Message successfully sent
        msg_snd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg_snd.sendto(msg.encode(), (UDP_ID, TX_PORT))
        return True
    except:
        return False


while(True):
    print("Type a message in the console to be sent from the gs")
    s = input()
    status = send(s)
    if(status):
        print("Message sent: {0}".format(s))
    else:
        print("Something went wrong")
