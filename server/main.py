#!/usr/bin/env python3
from groundstation import GroundStation
from settings import CREDENTIALS, DATABASE_URL

gs = GroundStation(CREDENTIALS, DATABASE_URL, 'messages', 'commands')
