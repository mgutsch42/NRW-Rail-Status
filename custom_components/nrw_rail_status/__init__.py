"""NRW Rail Status integration."""

from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .api import NRWHimApi

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    session = async_get_clientsession(hass)
    api = NRWHimApi(session)

    async def async_update():
        try:
            return await api.fetch_messages()
        except Exception as err:
            raise UpdateFailed(f"Unexpected error fetching NRW HIM data: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="NRW Rail Status",
        update_method=async_update,
        update_interval=entry.options.get("scan_interval", 60),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop("coordinator")
    return unload_ok
