import time
import RPi.GPIO as GPIO
import logging
import requests
from systemd import journal
from lib.battery import Battery
from lib.battery import OutputProcessor

relais = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(relais, GPIO.OUT)

battery = Battery()
processor = OutputProcessor()

class HeatingRod:
    def __init__(self, ip):
        self.ip = ip

    def state(self):
        response = requests.get('http://' + self.ip + '/relay/0/status')
        return response.json()['ison']
    
    def turn_on(self):
        response = requests.get('http://' + self.ip + '/relay/0?turn=on')
        return response.json()
        
    def turn_off(self):
        response = requests.get('http://' + self.ip + '/relay/0?turn=off')
        return response.json()

heating_rod_1 = HeatingRod('192.168.190.32')
heating_rod_2 = HeatingRod('192.168.190.33')
heating_rod_3 = HeatingRod('192.168.190.34')

while True:
    output = battery.exec('pwrsys')
    processed = processor.process_pwr_sys(output)
    if 'System SOC' in processed:
        system_soc = processed['System SOC']
        system_curr = processed['System Curr']

        rod_1_on = heating_rod_1.state()
        journal.send("Current: " + str(system_curr) + 'mA; Battery: ' + str(system_soc) + '%; rod1: ' + str(rod_1_on))

        # Turning heating rods on
        if system_curr > 50000 and system_soc > 85:
            heating_rod_1.turn_on()
        if rod_1_on and system_curr > 47000:
            heating_rod_2.turn_on()
        if rod_1_on and system_soc == 100:
            heating_rod_1.turn_on()
            heating_rod_2.turn_on()
            heating_rod_3.turn_on()

        # Turning heating rods off
        if system_curr < 0 and system_soc < 94:
            heating_rod_1.turn_off()
            heating_rod_2.turn_off()
        if system_soc < 94:
            heating_rod_3.turn_off()

        # Turning relais on/off.
        if system_soc < 35:
            GPIO.output(relais, True)
        else:
            GPIO.output(relais, False)

    elif len(processed) == 0:
        # If the result seems to be empty, we force a reconnection by re-instantiating the class
        journal.send("Empty result: %s" % output)
        battery = Battery()
    else:
        journal.send("ERROR: %s" % output)
        print(output)
    time.sleep(60)
