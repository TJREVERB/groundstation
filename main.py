from groundstation import GroundStation
from settings import CREDENTIALS, DATABASE_URL

gs = GroundStation(CREDENTIALS, DATABASE_URL, 'messages', 'commands')
d = {'message': 'heee', 'sat_time': '157'}
