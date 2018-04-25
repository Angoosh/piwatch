import sys
import os

os.system("apt install pip zlib1g-dev libjpeg-dev")
os.system("pip install pyowm")
os.system("pip install psutil")
os.system("pip install git+https://github.com/rm-hull/luma.oled")
os.system("rm /usr/local/share/fonts")
os.system("mkdir /usr/local/share/fonts")
os.system("mv /home/pi/watch/FreeMono.ttf /usr/local/share/fonts")
