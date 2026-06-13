"""Data coordinator for the NRW Rail Status integration."""

from __future__ import annotations

import asyncio
import logging
import aiohttp
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, API_URL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NRWRailStatusCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Zuginfo.nrw."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )

        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        """Fetch data from the API."""
        try:
            async with self.session.get(API_URL, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"API returned status {response.status}")

                return await response.json()

        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout while fetching data") from err

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"HTTP error: {err}") from err

        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err
