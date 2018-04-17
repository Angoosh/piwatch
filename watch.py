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

# Weather station
if network():
	place = 'Pardubice'
	owm = pyowm.OWM('4612172c6662b19a70dc25af195666a0')

# Printing on the LCD
if network():
	observation = owm.weather_at_place(place+',CZ')
	w = observation.get_weather()
	t = str(w.get_temperature(unit='celsius'))
def drew():
	with canvas(device) as draw:
    		draw.text((0, 0), strftime("%H:%M"), font = font, fill = "white" )
		draw.text((63, 0), strftime(".%S"), font = fon, fill="white")
		draw.text((60, 19), strftime("%d-%m-%y"), font = fon, fill = "white" )
		if network():
			draw.text((0, 45), t[44:-19]+"C", font = font, fill = "white" )
			draw.text((0, 32), place, font = fon, fill = "white" )
		else:
			draw.text((0, 45), "network err", font=fon, fill="white")
		draw.text((105, 55), str(os.getpid()), font=pid, fill="white")
		draw.text((105, 47), "PID:", font=pid, fill="white")

while True:
	try:
		drew()
	except:
		pass
