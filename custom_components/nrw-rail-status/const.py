"""Constants for the NRW Rail Status integration."""

DOMAIN = "nrw_rail_status"

# API endpoint for Zuginfo.nrw (öffentliche JSON-Daten)
API_URL = "https://www.zuginfo.nrw/api/ris"

# Update-Intervall in Sekunden (z. B. alle 60 Sekunden)
DEFAULT_UPDATE_INTERVAL = 60

# Sensor-Namen
SENSOR_NAME = "NRW Rail Status"

# Attribute Keys
ATTR_LINE = "line"
ATTR_CATEGORY = "category"
ATTR_DESCRIPTION = "description"
ATTR_START = "start"
ATTR_END = "end"
ATTR_LAST_UPDATE = "last_update"
