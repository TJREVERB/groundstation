import subprocess

listen = subprocess.Popen(['gnome-terminal', '-x', 'python3', 'listen.py'])
transmit = subprocess.Popen(['gnome-terminal', '-x', 'python3', 'transmit.py'])
fullGroundstation = subprocess.Popen(['gnome-terminal', '-x', 'python3', 'TJ_Groundstation_USRP.py'])
listen.wait()
transmit.wait()
fullGroundstation.wait()
