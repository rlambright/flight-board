from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_API_KEY, CONF_AIRPORT, CONF_UPDATE_INTERVAL
import requests
from datetime import datetime
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    api_key = entry.data[CONF_API_KEY]
    airport = entry.data.get(CONF_AIRPORT, "DAB")
    update_interval = entry.data.get(CONF_UPDATE_INTERVAL, 30)

    sensor = FlightBoardSensor(api_key, airport)
    async_add_entities([sensor], update_before_add=True)

class FlightBoardSensor(Entity):
    def __init__(self, api_key, airport):
        self._attr_name = "Flight Board"
        self._attr_unique_id = "flight_board_sensor"
        self._attr_native_value = "Initializing..."
        self.api_key = api_key
        self.airport = airport
        self._attr_extra_state_attributes = {}

    @property
    def should_poll(self):
        return True

    def _fetch_flights(self, flight_type):
        url = f"https://aeroapi.flightaware.com/aeroapi/airports/{self.airport}/flights/{flight_type}"
        headers = {"x-apikey": self.api_key}
        params = {
            "max_pages": 1
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            flights = response.json().get("flights", [])
            return flights
        except Exception as e:
            _LOGGER.error(f"FlightBoard: error fetching {flight_type}: {e}")
            return []

    def update(self):
        arrivals = self._fetch_flights("arrivals")
        departures = self._fetch_flights("departures")

        _LOGGER.info(f"Fetched {len(arrivals)} arrivals and {len(departures)} departures.")

        all_flights = arrivals[:3] + departures[:3]
        all_flights.sort(key=lambda f: f.get("scheduled_out") or f.get("scheduled_in") or "")

        self._attr_native_value = datetime.now().isoformat()
        self._attr_extra_state_attributes = {
            "flights": all_flights
        }
