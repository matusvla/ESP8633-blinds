import machine
import usocket
import json
from time import sleep


relay1pin = machine.Pin(12, machine.Pin.OUT) #D6
relay2pin = machine.Pin(14, machine.Pin.OUT) #D5

class ConfigurationError(Exception):
    pass

def handlePins(pin1set, pin2set):
    if pin1set == "on":
        if pin2set == "on":
            raise ConfigurationError
        relay2pin.on()
        sleep(0.05)
        relay1pin.off()
        return
    if pin2set == "on":
        relay1pin.on()
        sleep(0.05)
        relay2pin.off()
        return
    relay1pin.on()
    relay2pin.on()

def listenAndServe(): 

    s = usocket.socket()          
    port = 12345                
    s.bind(('', port))         
    s.listen(5)   
    s.setblocking(True)           
    print("server prepared")
    while True: 
        c, _ = s.accept()
        request = c.recv(1024) #1024
        request = request.decode()
        body = c.recv(1024) #1024
        body = body.decode()
        try:
            y = json.loads(body)
            handlePins(y["pin1"], y["pin2"])
        except ConfigurationError:
            print("Invalid configuration")
            c.send('HTTP/1.0 400 Bad request\r\nContent-type: text\r\n\r\n')
            c.send('400 Bad request')
            c.close()
            continue
        except:
            print("Invalid request")
            c.send('HTTP/1.0 422 Unprocessable entity\r\nContent-type: text\r\n\r\n')
            c.send('422 Unprocessable entity')
            c.close()
            continue

        print('Header = %s' % request)
        print('Body = %s' % body)
        c.send('HTTP/1.0 200 OK\r\nContent-type: text\r\n\r\n')
        c.send('200 OK')
        c.close()
