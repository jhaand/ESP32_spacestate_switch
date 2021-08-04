#!/bin/sh
#
# Script to upload the space state code to the ESP32
# 
# Install rshell via the command 'pip3 install rshell' 

rshell -p /dev/ttyUSB0 -b 115200 cp main.py secrets.py /pyboard

