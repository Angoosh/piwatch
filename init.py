import sys
import os
from time import sleep


sleep(2)
#os.system("sh /home/pi/watch/start.sh")
os.system("cd /home/pi/watch")
os.system("python weather.py &")
print("Weather process started")
sleep(3)
os.system("python watch.py &")
os.system("cd /home/pi")
print("Watch process started")ext
