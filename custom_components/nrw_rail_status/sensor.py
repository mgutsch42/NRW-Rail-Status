"""Sensor platform for the NRW Rail Status integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_NAME


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([NRWRailStatusSensor(coordinator, entry)], True)


class NRWRailStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of the NRW Rail Status sensor."""

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = f"{entry.entry_id}_nrw_rail_status"

    @property
    def native_value(self) -> int:
        """Return the number of active disruptions."""
        data = self.coordinator.data
        if not data:
            return 0

        # Nur aktive Meldungen zählen
        return sum(1 for m in data if getattr(m, "active", False))

    @property
    def extra_state_attributes(self) -> dict:
        """Return attributes for the first disruption and full list."""
        data = self.coordinator.data
        if not data:
            return {}

        first = data[0]

        return {
            "first_id": first.id,
            "first_title": first.title,
            "first_text": first.text,
            "first_start": f"{first.start_date} {first.start_time}",
            "first_end": f"{first.end_date} {first.end_time}",
            "first_priority": first.priority,
            "first_comp": first.comp,
            "first_product": first.product,
            "first_active": first.active,

            # komplette Liste aller Meldungen als Dictionaries
            "messages": [
                {
                    "id": m.id,
                    "title": m.title,
                    "text": m.text,
                    "start": f"{m.start_date} {m.start_time}",
                    "end": f"{m.end_date} {m.end_time}",
                    "priority": m.priority,
                    "comp": m.comp,
                    "product": m.product,
                    "active": m.active,
                }
                for m in data
            ],
        }
