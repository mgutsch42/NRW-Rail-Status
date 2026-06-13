"""Data coordinator for the NRW Rail Status integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers import aiohttp_client

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

        session = aiohttp_client.async_get_clientsession(hass)
        self.api = NRWHimApi(session)

    async def _async_update_data(self):
        """Fetch data from the API with retry and error handling."""
        try:
            messages = await self.api.fetch_messages()

            # Prüfen, ob die API gültige Daten geliefert hat
            if not messages:
                raise UpdateFailed("API returned no messages (empty result).")

            return messages

        except UpdateFailed:
            raise

        except Exception as err:
            # HAFAS-spezifische Fehler erkennen
            err_str = str(err)

            if "hammError" in err_str:
                raise UpdateFailed("HAFAS returned hammError (invalid session or payload).")

            if "svcResL" in err_str and "[]" in err_str:
                raise UpdateFailed("HAFAS returned empty svcResL (invalid request).")

            if "HCI" in err_str:
                raise UpdateFailed(f"HAFAS internal error: {err_str}")

            # Generischer Fehler
            raise UpdateFailed(f"Unexpected error fetching NRW HIM data: {err_str}") from err
