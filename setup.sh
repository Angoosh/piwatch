#!/bin/bash

apt install python-pip zlib1g-dev libjpeg-dev
pip install pyowm
pip install psutil
pip install git+https://github.com/rm-hull/luma.oled
rm /usr/local/share/fonts
mkdir /usr/local/share/fonts
mv /home/pi/watch/FreeMono.ttf /usr/local/share/fonts
