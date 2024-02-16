import schedule, time
import logging
from configuration import DomoticzConfiguration, GPIOBoardConfiguration
from domoticz_client import DomoticzClient
from dht11 import read
from lcd1602 import setup as setup_lcd, write as write_lcd
from ds18b20 import setup as setup_ds18b20, read as read_ds18b20
import os


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())
logger = logging.getLogger(__name__)

domoticz_config = DomoticzConfiguration()

gpio_board_config = GPIOBoardConfiguration()

client = DomoticzClient(
    base_url=domoticz_config.base_url,
    dht11_device_id=domoticz_config.dht11_device_id,
    username=domoticz_config.username,
    password=domoticz_config.password,
)

setup_lcd()
setup_ds18b20(ds18b20_serial_number=gpio_board_config.ds18b20_sensor_serial_number)

def read_data_and_publish():
    dht_11_values = read(gpio_pin=gpio_board_config.dht_11_sensor_pin)
    ds18b20_value =  read_ds18b20()
    text_first_line = ""
    text_second_line = ""
    if dht_11_values:
        text_first_line = f"{dht_11_values[1]} C, {dht_11_values[0]} %"
        client.send_dht11_temperature_data_json(
            temperature=dht_11_values[1],
            humidity=dht_11_values[0],
        )
    text_second_line = f"{ds18b20_value:.0f} C"
    write_lcd(
        text_first_line=text_first_line,
        text_second_line=text_second_line,
    )

schedule.every(30).seconds.do(read_data_and_publish)

while True:
    schedule.run_pending()
    time.sleep(1)
