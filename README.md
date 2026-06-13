# NRW Rail Status – Home Assistant Integration

Diese Integration zeigt aktuelle Störungen aus dem NRW‑Bahnnetz an.  
Datenquelle: https://www.zuginfo.nrw/api/ris

## Installation (HACS)

1. HACS → Integrationen → Custom repositories
2. URL: `https://github.com/mgutsch42/nrw-rail-status`
3. Typ: Integration
4. Installieren
5. Home Assistant neu starten
6. Integration hinzufügen: *NRW Rail Status*

## Sensor

Der Sensor liefert:

- **State:** Anzahl der aktuellen Störungen
- **Attribute (erste Störung):**
  - `line`
  - `category`
  - `description`
  - `start`
  - `end`
  - `last_update`
- **raw:** komplette JSON‑Liste aller Störungen

## Beispiel Dashboard

```yaml
type: entities
entities:
  - sensor.nrw_rail_status_sensor
