#!/usr/bin/env python3
from groundstation import GroundStation, Iridium
from settings import CREDENTIALS, DATABASE_URL

gs = GroundStation(CREDENTIALS, DATABASE_URL, 'messages', 'commands')
iridium = Iridium(CREDENTIALS, DATABASE_URL, 'messages', 'commands')