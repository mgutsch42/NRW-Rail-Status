# NRW Rail Status (Home Assistant Integration)

Diese Home‑Assistant‑Integration zeigt **aktuelle Störungen, Baustellen und Meldungen** aus dem nordrhein‑westfälischen Bahnnetz an.  
Die Daten stammen direkt aus **Zuginfo.nrw** und werden über die offizielle **HAFAS‑HIM‑Schnittstelle** abgerufen.

Die Integration ist vollständig lokal, benötigt keine Cloud‑Dienste und funktioniert ohne API‑Key.

---

## ✨ Features

- Echtzeit‑Abruf der NRW‑HIM‑Meldungen (Störungen, Baustellen, Ausfälle)
- Vollständige Auflösung aller HAFAS‑Referenzen:
  - betroffene **Bahnhöfe**
  - betroffene **Linien / Produkte**
  - betroffene **Streckenabschnitte**
  - zugehörige **Ereignisse**
- Anzeige der wichtigsten Informationen:
  - Titel, Beschreibung, Zeitraum
  - Priorität, Verbund, Produkt
  - vollständiger Text (HTML → Markdown)
- Sensor liefert:
  - Anzahl aktiver Störungen
  - Details zur ersten Störung
  - vollständige Liste aller Meldungen
- Dashboard‑kompatibel (Markdown, Entities, Custom Cards)
- HACS‑kompatibel

---

## 📦 Installation (HACS)

1. HACS öffnen  
2. **Integrationen → Custom Repositories**  
3. Repository hinzufügen:

   https://github.com/mgutsch42/nrw-rail-status

   Typ: **Integration**

4. Integration installieren  
5. Home Assistant neu starten  
6. Integration hinzufügen:

   **Einstellungen → Geräte & Dienste → Integration hinzufügen → „NRW Rail Status“**

---

## 🧠 Funktionsweise

Die Integration nutzt die gleiche API wie die Webseite **Zuginfo.nrw**:

- HAFAS‑Version: `1.24`
- Methode: `HimSearch`
- Region: `NRW`
- Client‑Emulation wie im Browser
- Session‑ID pro Request
- vollständige Referenzauflösung (`locL`, `prodL`, `edgeL`, `eventL`)

Die API‑Kommunikation erfolgt über `aiohttp` und ist vollständig asynchron.

---

## 🧩 Sensor‑Datenstruktur

Der Sensor `sensor.nrw_rail_status_sensor` liefert:

### State

- Anzahl aktiver Störungen

### Attribute

- `first_id`
- `first_title`
- `first_text`
- `first_start`
- `first_end`
- `first_priority`
- `first_comp`
- `first_product`
- `first_active`
- `first_locations`
- `first_products`
- `first_edges`
- `first_events`
- `messages` (Liste aller Meldungen inkl. Referenzauflösungen)

---

## 📊 Beispiel‑Dashboard

title: NRW Rail Status  
icon: mdi:train  
cards:

  - type: entities  
    title: Übersicht  
    entities:  
      - entity: sensor.nrw_rail_status_sensor  
        name: Anzahl der Störungen  

  - type: markdown  
    title: Details zur ersten Störung  
    content: |
      {% set msgs = state_attr('sensor.nrw_rail_status_sensor', 'messages') %}
      {% if msgs %}
      {% set first = msgs[0] %}

      ### **{{ first.title }}**

      **Beschreibung:**  
      {{ first.text }}

      **Beginn:** {{ first.start_date }} {{ first.start_time }}  
      **Ende:** {{ first.end_date }} {{ first.end_time }}

      **Priorität:** {{ first.priority }}  
      **Verbund:** {{ first.comp }}  
      **Produkt:** {{ first.product }}

      **Bahnhöfe:**  
      {{ first.locations }}

      {% else %}
      Keine aktuellen Störungen.
      {% endif %}

---

## 🛠 Dateien & Architektur

custom_components/nrw_rail_status/  
│  
├── __init__.py          → Integration Setup  
├── api.py               → HAFAS‑API‑Client + NRWMessage  
├── coordinator.py       → UpdateCoordinator  
├── sensor.py            → Sensor‑Definition  
├── const.py             → Konstanten  
├── config_flow.py       → UI‑Konfiguration  
├── manifest.json        → HA‑Manifest  
└── translations/        → Lokalisierung  

---

## 🧪 Debugging

logger:  
  default: warning  
  logs:  
    custom_components.nrw_rail_status: debug  

---

## 📄 Lizenz

MIT License

---

## ❤️ Autor

**Martin Gutsch**  
GitHub: https://github.com/mgutsch42
**Martin Gutsch**  
GitHub: https://github.com/mgutsch42
