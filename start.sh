#!/bin/bash

cd /home/pi/watch
python weather.py &
echo "Weather process started"

sleep 3

python watch.py &
cd /home/pi

echo "Watch process started"
