"""NRW Rail Status Integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import NRWRailStatusCoordinator

# Die Plattformen, die geladen werden sollen (in unserem Fall nur "sensor")
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration via configuration.yaml (Legacy/Optional)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # 1. Coordinator erstellen und dem Setup übergeben
    coordinator = NRWRailStatusCoordinator(hass, entry)
    
    # 2. Den ersten Datenabruf beim Start erzwingen (damit sofort Daten da sind)
    await coordinator.async_config_entry_first_refresh()

    # 3. Den Coordinator so im System speichern, wie es deine sensor.py erwartet
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator
    }

    # 4. Die sensor.py (Sensor-Plattform) anstupsen und laden
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration."""
    # 1. Die Sensor-Plattform sauber entladen
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    # 2. Die Daten aus dem Speicher von Home Assistant löschen
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
