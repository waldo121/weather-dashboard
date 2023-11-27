# From Sunfounderkit v2
import time
import smbus2 as smbus

BUS = smbus.SMBus(1)

def _write_word(addr, data):
	global BLEN
	temp = data
	if BLEN == 1:
		temp |= 0x08
	else:
		temp &= 0xF7
	BUS.write_byte(addr ,temp)

def _send_command(comm):
	# Send bit7-4 firstly
	buf = comm & 0xF0
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	_write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	_write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (comm & 0x0F) << 4
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	_write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	_write_word(LCD_ADDR ,buf)

def _send_data(data):
	# Send bit7-4 firstly
	buf = data & 0xF0
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	_write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	_write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (data & 0x0F) << 4
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	_write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	_write_word(LCD_ADDR ,buf)

def _init(addr, bl):
    # Takes slave address, and background light
#	global BUS
#	BUS = smbus.SMBus(1)
	global LCD_ADDR
	global BLEN
	LCD_ADDR = addr
	BLEN = bl
	try:
		_send_command(0x33) # Must initialize to 8-line mode at first
		time.sleep(0.005)
		_send_command(0x32) # Then initialize to 4-line mode
		time.sleep(0.005)
		_send_command(0x28) # 2 Lines & 5*7 dots
		time.sleep(0.005)
		_send_command(0x0C) # Enable display without cursor
		time.sleep(0.005)
		_send_command(0x01) # Clear Screen
		BUS.write_byte(LCD_ADDR, 0x08)
	except:
		return False
	else:
		return True

def _clear():
	_send_command(0x01) # Clear Screen

def _openlight():  # Enable the backlight
	BUS.write_byte(0x27,0x08)
	BUS.close()

def _write(x: int, y: int, txt: str):
	if x < 0:
		x = 0
	if x > 15:
		x = 15
	if y <0:
		y = 0
	if y > 1:
		y = 1

	# Move cursor
	addr = 0x80 + 0x40 * y + x
	_send_command(addr)

	for char in txt:
		_send_data(ord(char))

def setup():
    _init(0x27, 1) # init(slave address, background light)

def write(text: str):
    _write(0, 0, text)
