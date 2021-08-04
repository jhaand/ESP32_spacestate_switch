#!/bin/sh 
# Script to get an interactive prompt with the ESP32. You can use a
# different terminal program if you wish. 
# 
# Install rshell via: 'pip3 install rshell'

rshell -p /dev/ttyUSB0 -b 115200 repl
