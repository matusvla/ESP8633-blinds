import uos, machine
import gc
import webrepl
import json
import sys

webrepl.start()
gc.collect()

# custom code

configName = 'config.json'

def do_connect(ssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            password
    print('network config:', sta_if.ifconfig())


print('boot.py loaded')
print('loading config file')
try:
    json_file = open(configName, 'rb')
except OSError:
    print("could not open/read config file: ", configName)
    sys.exit(1)
with json_file:
    data = json.load(json_file)
    try:
        do_connect(data['ssid'], data['pass'])
    except:
        print("invalid config file: ", configName)
        sys.exit(1)

print('turning all pins off')
for pin in [machine.Pin(i, machine.Pin.OUT) for i in (0, 2, 4, 5, 12, 13, 14, 15)] :
    pin.on()
print('starting server')

import relay
relay.listenAndServe()
print('exit')