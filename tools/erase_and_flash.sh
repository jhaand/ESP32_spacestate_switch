#!/bin/sh
# Script to erase an ESP32 and install Micropython. Update this script
# to the latest version of Micropython and put the .bin file it in 
# from where you call this script the directory 
PORT="/dev/ttyUSB0" 

esptool.py --chip esp32 --port $PORT erase_flash
esptool.py --chip esp32 --port $PORT --baud 460800 write_flash -z 0x1000 esp32-idf3-*.bin
