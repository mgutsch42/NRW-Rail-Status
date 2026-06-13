"""Sensor platform for the NRW Rail Status integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    SENSOR_NAME,
    ATTR_LINE,
    ATTR_CATEGORY,
    ATTR_DESCRIPTION,
    ATTR_START,
    ATTR_END,
    ATTR_LAST_UPDATE,
)
from .coordinator import NRWRailStatusCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN].get("coordinator")

    if coordinator is None:
        coordinator = NRWRailStatusCoordinator(hass)
        hass.data[DOMAIN]["coordinator"] = coordinator
        await coordinator.async_refresh()

    async_add_entities([NRWRailStatusSensor(coordinator)], True)


class NRWRailStatusSensor(SensorEntity):
    """Representation of the NRW Rail Status sensor."""

    def __init__(self, coordinator: NRWRailStatusCoordinator) -> None:
        self._coordinator = coordinator
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = "nrw_rail_status_sensor"

    @property
    def native_value(self):
        """Return the number of disruptions."""
        data = self._coordinator.data
        if not data:
            return None

        # Anzahl der Störungen (z. B. length of list)
        return len(data)

    @property
    def extra_state_attributes(self):
        """Return detailed attributes."""
        data = self._coordinator.data
        if not data:
            return {}

        # Beispiel: Wir nehmen den ersten Eintrag als Detail
        first = data[0] if isinstance(data, list) and data else {}

        return {
            ATTR_LINE: first.get("line"),
            ATTR_CATEGORY: first.get("category"),
            ATTR_DESCRIPTION: first.get("description"),
            ATTR_START: first.get("start"),
            ATTR_END: first.get("end"),
            ATTR_LAST_UPDATE: first.get("lastUpdate"),
        }

    @property
    def should_poll(self) -> bool:
        """Coordinator handles polling."""
        return False

    async def async_update(self):
        """Update via coordinator."""
        await self._coordinator.async_request_refresh()
