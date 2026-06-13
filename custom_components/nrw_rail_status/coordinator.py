"""Data coordinator for the NRW Rail Status integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .api import NRWHimApi

_LOGGER = logging.getLogger(__name__)


class NRWRailStatusCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch HIM messages from Zuginfo.nrw."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )

        # Home Assistant stellt eine Session bereit → nutzen!
        self.api = NRWHimApi(hass.helpers.aiohttp_client.async_get_clientsession())

    async def _async_update_data(self):
        """Fetch data from the API."""
        try:
            messages = await self.api.fetch_messages()
            return messages

        except Exception as err:
            raise UpdateFailed(f"Error fetching NRW HIM data: {err}") from err
