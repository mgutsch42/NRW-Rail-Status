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
    coordinator: NRWRailStatusCoordinator = hass.data[DOMAIN]["coordinator"]

    async_add_entities([NRWRailStatusSensor(coordinator, entry)], True)


class NRWRailStatusSensor(CoordinatorEntity[NRWRailStatusCoordinator], SensorEntity):
    """Representation of the NRW Rail Status sensor."""

    def __init__(self, coordinator: NRWRailStatusCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = f"{entry.entry_id}_nrw_rail_status"

    @property
    def native_value(self) -> int | None:
        """Return the number of active disruptions."""
        data = self._coordinator.data
        if not data:
            return 0
        return len(data)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return attributes for the first disruption."""
        data = self._coordinator.data
        if not data:
            return {}

        first = data[0]

        return {
            ATTR_LINE: first.get("line"),
            ATTR_CATEGORY: first.get("category"),
            ATTR_DESCRIPTION: first.get("description"),
            ATTR_START: first.get("start"),
            ATTR_END: first.get("end"),
            ATTR_LAST_UPDATE: first.get("lastUpdate"),
            "raw": data,
        }
