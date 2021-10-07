# class for listening for messages for gs
from threading import Thread
import socket


class Listen:
    """
    Listen class used as object in main.py 
    Allows for threading to listen
    Returns all messages received
    """

    def __init__(self, listen_list):
        self.message_list = listen_list

    def get_list(self):
        return self.message_list

    def reset_list(self):
        self.message_list = []

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
                self.message_list.append(message_received)
