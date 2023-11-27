import schedule, time
import logging
from configuration import DomoticzConfiguration, GPIOBoardConfiguration
from domoticz_client import DomoticzClient
from dht11 import read_dht11_dat
from lcd1602 import setup, write
import os


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())
logger = logging.getLogger(__name__)

domoticz_config = DomoticzConfiguration()

gpio_board_config = GPIOBoardConfiguration()

client = DomoticzClient(
    base_url=domoticz_config.base_url,
    weather_device_id=domoticz_config.weather_device_id,
    username=domoticz_config.username,
    password=domoticz_config.password,
)

setup()
def read_data_and_publish():
    values = read_dht11_dat(gpio_board_config.weather_sensor_pin)
    logger.debug(values)
    if values:
        logger.info("Valid data from sensor")
        write(f"{values[1]} C, {values[0]} %")
        client.send_weather_data_json(
            temperature=values[1],
            humidity=values[0],
        )
    else:
        logger.error("Invalid data from sensor")

schedule.every(30).seconds.do(read_data_and_publish)

while True:
    schedule.run_pending()
    time.sleep(1)
