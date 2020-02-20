from threading import Thread
import socket

class APRS:
    """
    Listen class used as object in main.py 
    Allows for threading to listen
    Returns all messages received
    """

    def __init__(self, call_back: callable):
        self.callback = call_back
        self.start_thread()


    def start_thread(self):
        """
        Starts a thread to listen for new messages
        """
        listen_thread = Thread(target=self.run, args=())
        listen_thread.daemon = True
        listen_thread.start()

    def run(self):
        """
        Thread that continiously listens for new messages using sockets
        Adds the received message to the message list
        Checks to see if message was sent by us
        """
        UDP_ID = "127.0.0.1"
        RX_PORT = 5557
        while True:
            msg_lstn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg_lstn.bind((UDP_ID, RX_PORT))
            message_received = msg_lstn.recvfrom(1024)
            if "to SATT4" in str(message_received):
                self.callback(message_received)


#class Iridium:
