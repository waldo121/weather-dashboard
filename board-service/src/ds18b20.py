#!/usr/bin/env python3
#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
# Adapted from sunfounderkit v2, 26_ds18b20.py
#----------------------------------------------------------------
import os
import logging
import math

ds18b20 = ''

logger = logging.getLogger(__name__)

def setup(ds18b20_serial_number: str):
	global ds18b20
	if ds18b20_serial_number not in os.listdir('/sys/bus/w1/devices'):
		raise RuntimeError(f"The ds18b20 device with serial number {ds18b20} is not accessible. Validate file permissions")
	ds18b20 = ds18b20_serial_number


def read():
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	try:
		tfile = open(location)
		text = tfile.read()
		tfile.close()
	except Error:
		logger.error("Unable to read temperature")
		return math.nan
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature
