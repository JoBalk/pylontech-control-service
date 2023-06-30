import serial
import threading
import time
from systemd import journal

class Battery:
    ser = serial.Serial('/dev/ttyUSB0')
    ser.baudrate = 115200

    def __init__(self):
        self.__connect()

    # Private: Checks for existing connection and establish one if necessary.
    def __connect(self):
        journal.send("Connecting...")
        # For connecting to the batteries, we need to set the baudrate to 1200
        self.ser.baudrate = 1200
        # Now we need to send this magic command.
        self.ser.write(b"~20014682C0048520FCC3\r")
        time.sleep(1)
        # Set the baudrate back
        self.ser.baudrate = 115200
        time.sleep(1)
        # Logs in into admin mode
        self.ser.reset_input_buffer()
        self.ser.write("login debug".encode('ascii'))
        self.ser.write(b"\n")
        time.sleep(1)
        self.ser.reset_input_buffer()

    # Public: Reads from the serial input.
    def read(self):
        # Check for open connection first.
        if not self.ser.isOpen():
            self.__connect()
        output = ''
        # Reads until the output ends.
        while True:
            # Serial read
            cc = self.ser.readline()
            # Convert this to something useful.
            line = cc.strip().decode("utf-8")
            if len(line) > 0:
                # Nobody know why, but this is the end of the output.
                if line == "$$":
                    break
                output += line + "\n"
            else:
                # Waits for the next line.
                time.sleep(1)
        return output

    # Public: Executes command at the batteries
    def exec(self, command):
        # Check for open connection first.
        if not self.ser.isOpen():
            self.__connect()
        # Writes command to the batteries.
        journal.send('Executing Command: ' + command)
        self.ser.write(command.encode('ascii'))
        # Ends the Command.
        self.ser.write(b"\n")
        return self.read()

class OutputProcessor:
    def process_pwr_sys(self, output):
        processed = {}
        for line in output.splitlines():
            values = line.split(':')
            if len(values) == 2:
                key = values[0].strip()
                value = ''.join(c for c in values[1] if c.isdigit())
                processed[key] = int(value)
        return processed
