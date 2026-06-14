"""NRW Rail Status integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .api import NRWHimApi

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up NRW Rail Status from a config entry."""

    _LOGGER.debug("Setting up NRW Rail Status integration")

    session = async_get_clientsession(hass)
    api = NRWHimApi(session)

    async def async_update():
        try:
            data = await api.fetch_messages()
            _LOGGER.debug("Fetched %s HIM messages", len(data) if data else 0)
            return data
        except Exception as err:
            _LOGGER.error("Error fetching NRW HIM data: %s", err)
            raise UpdateFailed(f"Unexpected error fetching NRW HIM data: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="NRW Rail Status",
        update_method=async_update,
        update_interval=timedelta(
            seconds=entry.options.get("scan_interval", 60)
        ),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload NRW Rail Status config entry."""

    _LOGGER.debug("Unloading NRW Rail Status integration")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop("coordinator", None)

    return unload_ok
