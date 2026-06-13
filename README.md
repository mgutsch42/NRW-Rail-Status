NRW Rail Status – Home Assistant Integration
Diese Home‑Assistant‑Integration sollte aktuelle Störungen und Meldungen aus dem NRW‑Bahnnetz anzeigen.
Die Daten stammten ursprünglich von der öffentlichen API von Zuginfo.nrw.

⚠️ Aktueller Hinweis (Juni 2026)
Die bisher verwendete Datenquelle
https://www.zuginfo.nrw/api/ris  
liefert seit Kurzem dauerhaft den HTTP‑Status 404 – Not Found.

Damit ist die API nicht mehr erreichbar und die Integration kann aktuell
keine Störungsdaten laden. Die Einrichtung in Home Assistant schlägt deshalb mit einem Einrichtungsfehler fehl.

Die Integration selbst funktioniert technisch korrekt – die Ursache liegt ausschließlich in der nicht mehr verfügbaren API.

Es wird derzeit geprüft, ob alternative Datenquellen (z. B. DB Transport REST API, NRW OpenData oder eine mögliche neue Zuginfo‑API) genutzt werden können.
Sobald eine stabile Quelle verfügbar ist, wird die Integration entsprechend aktualisiert.

🚆 Funktionsumfang (ursprüngliche Version)
Abfrage der öffentlichen RIS‑API von Zuginfo.nrw

Automatische Aktualisierung alle 60 Sekunden

Sensor liefert:

State: Anzahl der aktuellen Störungen

Attribute: Details zur ersten Störung

raw: komplette JSON‑Liste aller Störungen (für Dashboards)

Hinweis: Dieser Funktionsumfang ist derzeit nicht nutzbar, da die API nicht mehr erreichbar ist.

📦 Installation über HACS
HACS → Integrationen

Rechts oben: Custom repositories

Folgende URL eintragen:

https://github.com/mgutsch42/nrw-rail-status

Typ: Integration

Repository hinzufügen

Integration installieren

Home Assistant neu starten

Integration hinzufügen: NRW Rail Status

Hinweis: Die Einrichtung schlägt aktuell fehl, da die API nicht erreichbar ist.

🧩 Sensor‑Details (ursprüngliche Version)
Sensor: sensor.nrw_rail_status_sensor
State:

Anzahl der aktuellen Störungen

Attribute (erste Störung):

Attribut	Bedeutung
line	Linienbezeichnung
category	Kategorie der Störung
description	Beschreibung
start	Beginn
end	Ende (falls bekannt)
last_update	Zeitstempel der letzten Aktualisierung
raw	komplette JSON‑Liste aller Störungen


Hinweis: Dieser Sensor wird aktuell nicht erzeugt, da die API nicht erreichbar ist.

📊 Beispiel‑Dashboard (Lovelace)
yaml
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
      content: 
        ```
