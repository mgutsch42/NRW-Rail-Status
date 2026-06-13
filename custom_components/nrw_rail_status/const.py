"""Constants for the NRW Rail Status integration."""

DOMAIN = "nrw_rail_status"

# API endpoint for Zuginfo.nrw (öffentliche JSON-Daten)
API_URL = "https://www.zuginfo.nrw/api/ris?format=json"

# Update-Intervall in Sekunden
DEFAULT_UPDATE_INTERVAL = 60

# Sensor-Name
SENSOR_NAME = "NRW Rail Status"

# Attribute Keys
ATTR_LINE = "line"
ATTR_CATEGORY = "category"
ATTR_DESCRIPTION = "description"
ATTR_START = "start"
ATTR_END = "end"
ATTR_LAST_UPDATE = "last_update"

# Liste aller Attribute (Best Practice)
ATTRIBUTES = [
    ATTR_LINE,
    ATTR_CATEGORY,
    ATTR_DESCRIPTION,
    ATTR_START,
    ATTR_END,
    ATTR_LAST_UPDATE,
]
