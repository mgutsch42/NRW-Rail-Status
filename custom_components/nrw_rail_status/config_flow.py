"""Config flow for NRW Rail Status integration."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN


class NRWConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NRW Rail Status."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="NRW Rail Status", data={})

        return self.async_show_form(step_id="user", data_schema=None)
