from typing import Dict
import httpx
import base64
import logging

logger = logging.getLogger(__name__)

class DomoticzClient:
    def __init__(
        self,
        base_url: str,
        dht11_device_id: int,
        username: str,
        password: str,
    ) -> None:
        self._base_url = base_url
        self._dht11_device_id = dht11_device_id
        self._authorization_token = base64.b64encode(bytes(f"{username}:{password}", 'utf-8')).decode()

    def send_dht11_temperature_data_json(
        self,
        temperature: float,
        humidity: float,
    ) -> None:
        with httpx.Client(headers={"Authorization": f"Basic {self._authorization_token}"}) as client:
            response = client.get(f"{self._base_url}/json.htm?type=command&param=udevice&idx={self._dht11_device_id}&nvalues=0&svalue={temperature};{humidity};0")
