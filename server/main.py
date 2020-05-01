#!/usr/bin/env python3
from groundstation import GroundStation, Iridium
from settings import CREDENTIALS, DATABASE_URL
import os
import threading


def start_server():
    gs = GroundStation(CREDENTIALS, DATABASE_URL,
                       'messages', 'commands')
    iridium = Iridium(CREDENTIALS, DATABASE_URL,
                      'messages', 'commands', 'iridium')


def start_react():
    os.chdir(os.pardir)
    os.chdir("client")
    os.system("npm start")


if(__name__ == '__main__'):
    """
    Starts both server and react app at the same time
    """
    t1 = threading.Thread(target=start_server, args=())
    t2 = threading.Thread(target=start_react, args=())
    t1.start()
    t2.start()
