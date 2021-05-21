import socket


def send(msg: str) -> bool:
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
