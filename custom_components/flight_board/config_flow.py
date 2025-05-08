from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_API_KEY, CONF_AIRPORT, CONF_UPDATE_INTERVAL, DEFAULT_AIRPORT, DEFAULT_UPDATE_INTERVAL

class FlightBoardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Flight Board", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Optional(CONF_AIRPORT, default=DEFAULT_AIRPORT): str,
            vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
