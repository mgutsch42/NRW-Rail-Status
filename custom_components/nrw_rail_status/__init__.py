"""NRW Rail Status Integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import NRWRailStatusCoordinator


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration via configuration.yaml (optional)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""

    coordinator = NRWRailStatusCoordinator(hass)

    # Coordinator zuerst speichern
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["coordinator"] = coordinator

    # Erster Refresh mit Fehlerbehandlung
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        # Integration trotzdem laden, Coordinator versucht später erneut
        coordinator.logger.warning(
            "Initial data refresh failed: %s. Will retry automatically.", err
        )

    # Plattformen laden
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    if unload_ok:
        hass.data[DOMAIN].pop("coordinator", None)

    return unload_ok
