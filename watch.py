from time import sleep, gmtime, strftime
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pyowm
import os
import urllib2
import RPi.GPIO as GPIO
import psutil

# State of render
s = 0

# Inderrupts
def menuadd(channel):
        global s
        s+=1
def menusub(channel):
        global s
        s-=1


# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(21, GPIO.FALLING, callback=menuadd, bouncetime=300)
GPIO.add_event_detect(20, GPIO.FALLING, callback=menusub, bouncetime=300)

# Network
def network():
        try:
                urllib2.urlopen('http://216.58.192.142', timeout=1)
                return True
        except urllib2.URLError as err:
                return False

a = network()
# LCD
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)
font = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 22, encoding="unic")
fon = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 14, encoding="unic")
pid = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 8, encoding="unic")
fond = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 40, encoding="unic")

# Weather station
place = 'Pardubice'
owm = pyowm.OWM('4612172c6662b19a70dc25af195666a0')

# Printing on the LCD
if network() and s == 1:
        observation = owm.weather_at_place(place+',CZ')
        w = observation.get_weather()
        t = str(w.get_temperature(unit='celsius'))
def second():
        if network() and s == 1:
                observation = owm.weather_at_place(place+',CZ')
                w = observation.get_weather()
                t = str(w.get_temperature(unit='celsius'))
                list = t.split(',')
                lst = list[2].split(': ')
        with canvas(device) as draw:
                draw.text((0, 0), strftime("%H:%M"), font = font, fill = "white" )
                draw.text((63, 0), strftime(".%S"), font = fon, fill="white")
                draw.text((60, 19), strftime("%d-%m-%y"), font = fon, fill = "white" )
                if network():
                        draw.text((0, 45), lst[1]+"C", font = font, fill = "white" )
                        draw.text((0, 32), place, font = fon, fill = "white" )
                else:
                        draw.text((0, 45), "network err", font=fon, fill="white")

def first():
        if network() and s == 1:
                observation = owm.weather_at_place(place+',CZ')
                w = observation.get_weather()
                t = str(w.get_temperature(unit='celsius'))
                list = t.split(',')
                lst = list[2].split(': ')
        with canvas(device) as draw:
                draw.text((0, 0), strftime("%H:%M"), font = fond, fill="white")
                draw.text((0, 40), strftime("%d-%m-%y"), font = fon, fill="white")
                if GPIO.input(26)==0:
                        while GPIO.input(16)==1:
                                device.clear()

def third():
        if network() and s == 1:
                observation = owm.weather_at_place(place+',CZ')
                w = observation.get_weather()
                t = str(w.get_temperature(unit='celsius'))
                list = t.split(',')
                lst = list[2].split(': ')
        with canvas(device) as draw:
                draw.text((105, 47), "PID:", font=pid, fill="white")
                draw.text((105, 55), str(os.getpid()), font=pid, fill="white")
                draw.text((0, 0), "CPU:"+str(psutil.cpu_percent())+"%", font=font, fill="white")
                draw.text((0, 30), "shutdown:", font=fon, fill="white")
                draw.text((0, 40), "reboot:", font=fon, fill="white")
                if GPIO.input(16)==0:
                        device.clear()
                        os.system("sudo shutdown now")
                elif GPIO.input(26)==0:
                        device.clear()
                        os.system("sudo reboot")
while True:
        try:
                if s==0:
                        first()
                elif s==1:
                        second()
                elif s==2:
                        third()

                if s<0:
                        s = 0
                if s>2:
                        s = 2
        except:
                pass
