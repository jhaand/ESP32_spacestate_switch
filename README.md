This project documents how to make a spacestate switch, connect it to
the internet and make sure that the whole of hackerdom can see it. 

# Introduction

Most Hackerspaces andmakerspaces want the rest of the world to know that
people are there. This is done via the Spacestate switch near the
entrance of the door.  When someone comes in, they flip the switch and a
websites like https://mapall.space and https://hackerspaces.nl can show
that the space is open.  When the last person leaves, flip the switch
off and the rest of the world can see that nobody's home. 

# Hardware

You can also make a simple version with the following items.
 * NodeMCU with ESP32
 * Toggle switch
 * Breadboard
 * USB phone charger
 * USB cable, USB-A to micro USB
 * one 10K resistor

In order to create a more fancy space state switch you will need the following components:  
 * NodeMCU with ESP32
 * Some perfboard
 * Pinheader Sockets 
 * USB phone charger
 * USB cable, USB-A to micro USB
 * Nice box with a transparent cover to place the board in
 * BC547 small signal NPN transistor
 * LEDs: RED, Blue, Yellow and Green
 * Some resistors
 * A big impressive knife switch

This version will look more awesome, has status LEDs, a nice box  and
the switch is somewhat isolated from the NodeMCU. It will also has the
input reversed as described. So you will need to change the code a bit. 

# Software 
The space state switch runs on MicroPython the Switch side and PHP on
the server side.  A web server that will serve the 'spaceapi.json' file
to everyone. The server needs to be world wide reachable and
configurable by the deployer of the spacestate. Fortunately the traffic
will not be that high. So it's even possible to run it at home. 

## SpaceAPI.json
The webserver will serve a file with the most important data about your
makerspace. Not just if someone's there or not. The spaceapi.json for
Hackerspace TDvenlo can be found on
https://spaceapi.tdvenlo.nl/spaceapi.json The server is our main server
in our hackerspace, we use the DNS subdomain capability of our main site
hosting to point to this location. 

If you write a spaceapi.json make sure you have a backup. Because if you
test the software, it will get written over. So make sure that the
source file in the PHP  hosts the correct information.  Next to the
spaceapi.json, provide a logo for when the space remains open and when
it remains closed. These should consist of small PNG files that can be
reached over the internet.  

https://spaceapi.io has more information on how to create your own
spaceapi.json file.  You can find all the other spaceapi.json files
world wide in the spaceapi directory
https://github.com/SpaceApi/directory 

## Micropython on the NodeMCU
The NodeMCU will use Micropython to read the status of the switch and
forward the status to the webserver. 

## WebServer side
On your webserver you will need to do the following. 

### PHP code
The PHP code will overwrite your spaceapi.json every time. Changing between the file spaceapi_open.json and spaceapi_closed.json each time. 

### Webserver
As is described on https://spacapi.io, your webserver needs to provide
CORS and Content-type. This is not everywhere in place, so you need
control ver the server that will host the spaceapi.json. 
Of course your webserver needs to run PHP with at least version 7.2 in order to use this package. 

# Updating the global registry

The repository https://github.com/SpaceApi/directory lists all the
global hackerspaces. Add you hackerspace and the URL of you
spaceapi.json via a pull request on github. You can find more
information here: https://spaceapi.io/provide-an-endpoint/

# Resources 

https://spaceapi.io

https://spaceapi.vanheusden.com/

https://hackerspaces.nl/ 

https://mapall.space

Android app: MyHackerspace
https://spaceapi.io/stuff/my-hackerspace/
https://play.google.com/store/apps/details?id=ch.fixme.status

# FAQ

Q: Why use an ESP32 instead of a ESP8266  ?  
A: The ESP32 is more stable and has a watchdog. If the NodeMCU hangs,
then the watchdog will reset the NodeMCU. So that you always have the
correct state. The ESP32 allows also more GPIO's and has more ROM to
store your memory. 

Q: can I use other methods for writing the spaceapi.json?  
A: You can use any solution you like. We currently use home-assistant in
our space. Which also allows remote operation and only needs a single
URL call to change the state. This is only an example.

Q: Can we switch the space state remotely?  
A: During the first Covid lockdown we used a remote PHP form to switch
the space-state remotely. This is included in ths repository. This PHP
script will perform the same call as the NodeMCU. It will keep the same
state until either the script is run again or the switch on the NodeMCU
is toggled. 
