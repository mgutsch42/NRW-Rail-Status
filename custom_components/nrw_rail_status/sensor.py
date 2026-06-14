"""Sensor platform for NRW Rail Status."""

from __future__ import annotations

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the NRW Rail Status sensor."""
    coordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([NRWRailStatusSensor(coordinator)], True)


class NRWRailStatusSensor(CoordinatorEntity, SensorEntity):
    """Sensor that exposes the number of active disruptions."""

    _attr_name = "NRW Rail Status"
    _attr_icon = "mdi:train"
    _attr_unique_id = "nrw_rail_status_sensor"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def state(self):
        """Return number of active disruptions."""
        data = self.coordinator.data

        if not data:
            _LOGGER.debug("Sensor state: no data available, returning 0")
            return 0

        active_count = len([m for m in data if m.active])
        _LOGGER.debug("Sensor state: %s active disruptions", active_count)
        return active_count

    @property
    def extra_state_attributes(self) -> dict:
        """Return detailed attributes for the first disruption and full list."""
        data = self.coordinator.data

        if not data:
            _LOGGER.debug("Sensor attributes: no data available")
            return {}

        first = data[0]

        return {
            # Basisdaten der ersten Meldung
            "first_id": first.id,
            "first_title": first.title,
            "first_text": first.text,
            "first_start": f"{first.start_date} {first.start_time}",
            "first_end": f"{first.end_date} {first.end_time}",
            "first_priority": first.priority,
            "first_comp": first.comp,
            "first_product": first.product,
            "first_active": first.active,

            # Aufgelöste Referenzen
            "first_locations": first.locations,
            "first_products": first.products,
            "first_edges": first.edges,
            "first_events": first.events,

            # komplette Liste aller Meldungen
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
                    "locations": m.locations,
                    "products": m.products,
                    "edges": m.edges,
                    "events": m.events,
                }
                for m in data
            ],
        }
