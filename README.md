# Pylontech control service

A small implementation for controlling Pylontech batteries.
This project includes a damon which switches a raspberry PI output for a specific percentage of the battery system.
It also includes a telegram-bot which gives the data to the outside world.

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