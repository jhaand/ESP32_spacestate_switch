import network
import secrets
import machine
import time
import ntptime 
import ussl
import urequests as requests

# This file get the ESSID, WPA2-key and the spaceapi key from the file
# "secrets.py" 
# Change this to make it work in yur own hackerspace. 

print("SSID to connect to: " + secrets.wifi_SSID)
#print("Password to use: " + secrets.wifi_passwd)
# URL of the accessible spaceapi PHP file.  
url = "https://spaceapi.haxorspace.iets/spaceapi.php"

print("Password to use: " + secrets.API_key) 
led_post = machine.Pin(21, machine.Pin.OUT)   # Red 
led_wifi = machine.Pin(17, machine.Pin.OUT)   # Blue
led_sstate = machine.Pin(16, machine.Pin.OUT) # Yellow 
led_intern = machine.Pin(2, machine.Pin.OUT)

in_switch = machine.Pin(39, machine.Pin.IN)

# get wifi connection
def connect_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to Wifi')
        sta_if.active(True)
        sta_if.connect(secrets.wifi_SSID,secrets.wifi_passwd)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())
    led_wifi.on()

def read_switch(input=in_switch):
    state = input.value()
    return not state

def set_led_sstate(state=False):
    if state == True:
        led_sstate.on()
    else:
        led_sstate.off()

def set_json(state=False):
    headers = {'Content-Type': 'application/json'}
    state = str(state).lower()
    data = '{ "API_key":"%s", "sstate":"%s"} '% (secrets.API_key, state)
    print('State: ', state)
    r = requests.post(url, data=data, headers=headers)
    print(r.text)
    r.close()
    return True

# POST
for led_output in [led_post, led_wifi, led_sstate, led_intern]:
    led_output.on()
    time.sleep(0.2)
    led_output.off()

# The initialization of the Space state.  Blink some LEDs, connect to
# wifi and activate the watchdog. 
time.sleep(0.5)
led_post.on()
print("POST Passed")

connect_wifi()
ntptime.settime()

# Activate the watchdog
wdt = machine.WDT(timeout=5000)
wdt.feed()
    
# Initialize the space state
space_state = read_switch()
set_led_sstate(space_state)
led_intern_state = 1
_ = set_json(space_state)

while True:
    wdt.feed()
    space_state_old = space_state
    led_intern_state_old = led_intern_state
    time.sleep(0.200)
    space_state = read_switch()
    current_time = time.time()

    # Set the state for the onboard LED based on the time
    if (current_time % 7 == 0):
        led_intern_state = 1
    else:
        led_intern_state = 0

    # Change the output of the onboard LED based on the state
    if led_intern_state_old != led_intern_state:
        if led_intern_state == 1:
            led_intern.on()
        else:
            led_intern.off()

    # If the space state changes, do a lot of stuff. 
    if (space_state != space_state_old):
        t = time.localtime()
        strftime = name = '{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(t[0], t[1], t[2], t[3], t[4], t[5])
        print("time: ", strftime)
        print("State has changed to: ",str(space_state))
        set_led_sstate(space_state)
        _ = set_json(space_state)
        for i in range(10):
            time.sleep(0.3)
            wdt.feed()
        print("Waiting for new input")

