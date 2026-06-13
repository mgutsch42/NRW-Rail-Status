"""NRW Rail Status Integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import NRWRailStatusCoordinator


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via configuration.yaml (optional)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    coordinator = NRWRailStatusCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    # 🔥 WICHTIG: Sensor-Plattform laden!
    hass.config_entries.async_setup_platforms(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the integration."""
    hass.data[DOMAIN].pop("coordinator", None)
    return True
