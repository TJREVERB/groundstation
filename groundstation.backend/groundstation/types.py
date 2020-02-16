from enum import Enum


class ReceivedType(Enum):
    Echo = "echos"
    Beacon = "beacons"
    Dump = "dumps"
