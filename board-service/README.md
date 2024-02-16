
# Board Service

## Hardware

<!-- TODO: Update this image -->
![hardware setup](docs/images/setup.jpg)


Components:
- 1 x rpi model 3b
- 1 x dht11 temperature + humidity sensor
    - DATA pin -> GPIO pin 19
- 1 x lcd1602 i2c
- 1 x DS18B20 temperature sensor
    - DATA pin -> GPIO pin 4

## Raspberry pi configuration

### I2C interface

In order to talk to the lcd, the i2c interface must be enabled.

``` sh
sudo raspi-config
```

### DS18B20 sensor configuration

1. Upgrade the kernel] 
```sh
sudo apt-get update
sudo apt-get upgrade
```

1. In `/boot/config.txt`, add the following line to the bottom
```txt
dtoverlay=w1-gpio
```

1. Reboot
1. Mount the device drivers
```sh
sudo modprobe w1-gpio
sudo modprobe w1-therm
```
1. Check device is present, look for serial number of sensor
```sh
sudo ls /sys/bus/w1/devices
# ex. output, here `28-01192cd3d28f` is the serial number of the sensor 
28-01192cd3d28f  w1_bus_master1

```

## Software

This service will have the following responsibilities:

- acquiring data from sensors
- display information on lcd screen
- push information to domoticz

## Domoticz configuration

dht11:
    - Virtual sensor
    - device id must be passed to the board service through configuration

ds18b20:
    - 1-Wire sensor
    - OWSF Path is unset
    - Discovered automatically by domoticz

## Running the software

```sh
cp .env.template .env # don't forget to modify it
poetry run python src/app.py
```
## Systemd service configuration

```sh
sudo cp rpi-board.service /etc/systemd/system/rpi-board.service
sudo systemctl enable rpi-board
sudo systemctl start rpi-board
```