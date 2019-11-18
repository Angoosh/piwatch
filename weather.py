import pyowm
import urllib2
from time import sleep

def network():
	try:
        	urllib2.urlopen('http://216.58.192.142', timeout=1)
        	return True
	except urllib2.URLError as err:
        	return False

place = 'Pardubice'
owm = pyowm.OWM('f9c3cff3a93557a04c4c04b83bcdf1c6')

def main():
	if network():
		observation = owm.weather_at_place(place+',CZ')
		w = observation.get_weather()
		t = str(w.get_temperature(unit='celsius'))
		list = t.split(',')
		lst = list[2].split(': ')
		file = open("weather.info","w")
		file.write(lst[1])
		file.close()
	else:
		file = open("weather.info","w")
		file.write("NULL")
		file.close()
		sleep(3)
while True:
	try:
		main()
	except:
		pass
