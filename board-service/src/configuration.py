from pydantic_settings import BaseSettings, SettingsConfigDict

class DomoticzConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra = 'ignore')
    base_url: str
    dht11_device_id: int # for dht11 sensor
    username: str
    password: str

class GPIOBoardConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra = 'ignore')
    dht_11_sensor_pin: int
    ds18b20_sensor_serial_number: str
