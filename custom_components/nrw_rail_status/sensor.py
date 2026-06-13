"""Sensor platform for the NRW Rail Status integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_NAME,
)
from .coordinator import NRWRailStatusCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the sensor platform."""
    # Wir holen den Coordinator aus den Config-Einträgen (Best Practice für neuere HA-Versionen)
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities([NRWRailStatusSensor(coordinator)], True)


class NRWRailStatusSensor(CoordinatorEntity[NRWRailStatusCoordinator], SensorEntity):
    """Representation of the NRW Rail Status sensor."""

    def __init__(self, coordinator: NRWRailStatusCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_status"

    @property
    def native_value(self) -> int | None:
        """Return the number of active disruptions."""
        data = self._coordinator.data
        if data is None:
            return None

        # Der Zustand des Sensors ist die bloße Anzahl der aktuellen Störungen
        return len(data)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return all disruptions as a list for the dashboard."""
        data = self._coordinator.data
        if not data:
            return {"disruptions": []}

        # Wir übergeben die komplette Liste an das Attribut "disruptions"
        # Jedes Element in dieser Liste ist ein Dictionary mit line, category, description etc.
        return {
            "disruptions": data
        }
