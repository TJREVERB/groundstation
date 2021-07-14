import socket


def listen() -> str:
    """
    Returns the most recent message from the gs
    """
    UDP_ID = "127.0.0.1"
    RX_PORT = 5557
    msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg_lstn.bind((UDP_ID, RX_PORT))
    message_received = str(msg_lstn.recvfrom(1024))
    return message_received


while(True):
    print("Listening for messages")
    s = listen()
    print("Message received: {0}".format(s))
