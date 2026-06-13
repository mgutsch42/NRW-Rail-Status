# NRW Rail Status – Home Assistant Integration

Diese Home‑Assistant‑Integration zeigt aktuelle Störungen und Meldungen aus dem NRW‑Bahnnetz an.  
Die Daten stammen von der öffentlichen API von **Zuginfo.nrw**:  
https://www.zuginfo.nrw/api/ris

> **Hinweis: Diese Integration befindet sich aktuell in aktiver Entwicklung / Testphase.**  
> Funktionen können sich ändern, es können Fehler auftreten und nicht alle Datenpunkte sind final.  
> Rückmeldungen und Fehlerberichte sind ausdrücklich erwünscht.

---

## 🚆 Funktionsumfang

- Abfrage der öffentlichen RIS‑API von Zuginfo.nrw  
- Automatische Aktualisierung alle 60 Sekunden  
- Sensor liefert:
  - **State:** Anzahl der aktuellen Störungen
  - **Attribute:** Details zur *ersten* Störung
  - **raw:** komplette JSON‑Liste aller Störungen (für Dashboards)

---

## 📦 Installation über HACS

1. HACS → **Integrationen**
2. Rechts oben: **Custom repositories**
3. Folgende URL eintragen:

   https://github.com/mgutsch42/nrw-rail-status

4. Typ: **Integration**
5. Repository hinzufügen
6. Integration installieren
7. Home Assistant neu starten
8. Integration hinzufügen: **NRW Rail Status**  
   URL des Repositories: https://github.com/mgutsch42/nrw-rail-status

---

## 🧩 Sensor‑Details

### Sensor: `sensor.nrw_rail_status_sensor`

**State:**  
- Anzahl der aktuellen Störungen

**Attribute (erste Störung):**

| Attribut       | Bedeutung |
|----------------|-----------|
| `line`         | Linienbezeichnung |
| `category`     | Kategorie der Störung |
| `description`  | Beschreibung |
| `start`        | Beginn |
| `end`          | Ende (falls bekannt) |
| `last_update`  | Zeitstempel der letzten Aktualisierung |
| `raw`          | komplette JSON‑Liste aller Störungen |

---

## 📊 Beispiel‑Dashboard (Lovelace)

```yaml
title: NRW Rail Status
icon: mdi:train
cards:

  - type: entities
    title: Übersicht
    entities:
      - entity: sensor.nrw_rail_status_sensor
        name: Anzahl der Störungen

  - type: entity
    entity: sensor.nrw_rail_status_sensor
    name: Statusanzeige
    state_color: true

  - type: markdown
    title: Details zur ersten Störung
    content: |
      {% set s = states('sensor.nrw_rail_status_sensor') %}
      {% set a = state_attr('sensor.nrw_rail_status_sensor', 'description') %}
      {% set l = state_attr('sensor.nrw_rail_status_sensor', 'line') %}
      {% set c = state_attr('sensor.nrw_rail_status_sensor', 'category') %}
      {% set st = state_attr('sensor.nrw_rail_status_sensor', 'start') %}
      {% set e = state_attr('sensor.nrw_rail_status_sensor', 'end') %}
      {% set u = state_attr('sensor.nrw_rail_status_sensor', 'last_update') %}

      **Aktuelle Störungen:** {{ s }}

      {% if s|int > 0 %}
      **Linie:** {{ l }}
      **Kategorie:** {{ c }}
      **Beschreibung:** {{ a }}
      **Beginn:** {{ st }}
      **Ende:** {{ e }}
      **Letzte Aktualisierung:** {{ u }}
      {% else %}
      Keine aktuellen Störungen gemeldet.
      {% endif %}

  - type: conditional
    conditions:
      - entity: sensor.nrw_rail_status_sensor
        state_not: "0"
    card:
      type: markdown
      title: Alle Störungen (JSON-Rohdaten)
      content: |
        ```json
        {{ state_attr('sensor.nrw_rail_status_sensor', 'raw') }}
        ```
