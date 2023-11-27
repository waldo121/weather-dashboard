from pydantic_settings import BaseSettings, SettingsConfigDict

class DomoticzConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra = 'ignore')
    base_url: str
    weather_device_id: int
    username: str
    password: str

class GPIOBoardConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra = 'ignore')
    weather_sensor_pin: int
