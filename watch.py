from time import sleep, gmtime, strftime
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pyowm
import os

# LCD
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)
font = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 20, encoding="unic")
fon = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 14, encoding="unic")
pid = ImageFont.truetype("/usr/local/share/fonts/FreeMono.ttf", 8, encoding="unic")

# Weather station
place = 'Pardubice'
owm = pyowm.OWM('4612172c6662b19a70dc25af195666a0')
observation = owm.weather_at_place(place+',CZ')

# Printing on the LCD
while True:
	w = observation.get_weather()
	t = str(w.get_temperature(unit='celsius'))
	with canvas(device) as draw:
    		draw.text((0, 0), strftime("%H:%M:%S"), font = font, fill = "white" )
		draw.text((20, 16), strftime("%d-%m-%y"), font = fon, fill = "white" )
		draw.text((0, 45), t[44:-19]+"C", font = font, fill = "white" )
		draw.text((0, 32), place, font = fon, fill = "white" )
		draw.text((110, 55), str(os.getpid()), font=pid, fill="white")
		draw.text((110, 47), "PID:", font=pid, fill="white")
