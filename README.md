# Pylontech control service

A small implementation for controlling Pylontech batteries.
This project includes a damon which switches a raspberry PI output for a specific percentage of the battery system.
It also includes a telegram-bot which gives the data to the outside world.

This project can be used for home-automation. Especially for using the battery in an IOT-environment. 

## Usage

### The battery daemon

TBD

### The telegram bot

TBD

## Using the daemons

This repository includes two example daemons.

The example files need to be copied to `~/.config/systemd/user` and then they can used.

```bash
systemctl --user enable telegram.service
systemctl --user start telegram.service
systemctl --user enable battery.service
systemctl --user start battery.service
```

## Manual communication

For debugging purposes there is always the possibility to speak to the batteries manually.

### Initialization

After the initialization it is possible to execute the commands according to the official documentation.

```bash
stty -F /dev/ttyUSB0 1200 raw -echo
echo -ne "~20014682C0048520FCC3\r" > /dev/ttyUSB0
stty -F /dev/ttyUSB0 115200 raw -echo
echo -ne 'login debug\n' > /dev/ttyUSB0
```

### Executing commands

Baud rate needs to be at 115200.

```bash
stty -F /dev/ttyUSB0 115200 raw -echo
```
Executing commands:

```bash
echo -ne 'pwrsys\n' > /dev/ttyUSB0
echo -ne 'pwrs\n' > /dev/ttyUSB0
...
```

See the official Pylontech-documentation for the complete command list.

### Reading response from the batteries

Baud rate needs to be the same as on the executing site. So for normal commands it needs to be 115200.

```bash
stty -F /dev/ttyUSB0 115200 raw -echo
```

Reading from the battery-device:

```bash
cat -v /dev/ttyUSB0
```