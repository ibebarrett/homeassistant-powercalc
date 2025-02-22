from __future__ import annotations

import time

import requests

from .errors import PowerMeterError
from .powermeter import PowerMeasurementResult, PowerMeter


class TasmotaPowerMeter(PowerMeter):
    def __init__(self, device_ip: str) -> None:
        self._device_ip = device_ip

    def get_power(self) -> PowerMeasurementResult:
        r = requests.get(
            f"http://{self._device_ip}/cm?cmnd=STATUS+8",
            timeout=10,
        )
        json = r.json()

        try:
            power = json["StatusSNS"]["ENERGY"]["Power"]
        except KeyError:
            raise PowerMeterError("Unexpected JSON response format")

        return PowerMeasurementResult(float(power), time.time())
