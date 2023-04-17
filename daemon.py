import time
import RPi.GPIO as GPIO
import logging
from systemd import journal
from lib.battery import Battery
from lib.battery import OutputProcessor

relais = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(relais, GPIO.OUT)

battery = Battery()
processor = OutputProcessor()

while True:
    output = battery.exec('pwrsys')
    processed = processor.process_pwr_sys(output)
    if 'System SOC' in processed:
        system_soc = processed['System SOC']
        if system_soc > 45:
            GPIO.output(relais, False)
            journal.send("%s - AUS" % processed['System SOC'])
        elif system_soc < 40:
            GPIO.output(relais, True)
            journal.send("%s - AN" % processed['System SOC'])
    else:
        journal.send("ERROR: %s" % output)
        print(output)
    time.sleep(60)
