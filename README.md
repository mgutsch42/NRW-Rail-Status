# NRW Rail Status – Home Assistant Integration

Diese Home‑Assistant‑Integration zeigt aktuelle Störungen, Baustellen und Meldungen aus dem NRW‑Bahnnetz an.  
Die Daten stammen aus der offiziellen **Zuginfo.nrw‑HIM‑API** (HimSearch).

---

## 🚆 Funktionsumfang

- Live‑Abruf der NRW‑HIM‑API (HimSearch)
- Anzeige der **aktuellen Anzahl von Störungen**
- Detailinformationen zur **ersten Störung**
- Vollständige Liste aller Meldungen (Titel, Text, Zeitraum, Priorität, Verbund)
- Automatische Aktualisierung über einen Update‑Coordinator
- 100% kompatibel mit Standard‑Home‑Assistant‑Karten

---

## 📦 Installation über HACS (manuell)

1. HACS → **Integrationen**
2. Rechts oben: **Custom repositories**
3. Folgende URL eintragen:

   https://github.com/mgutsch42/nrw-rail-status

4. Typ: **Integration**
5. Repository hinzufügen
6. Integration installieren
7. Home Assistant neu starten
8. Integration hinzufügen: **NRW Rail Status**

---

## ⚙️ Konfiguration

Die Integration nutzt einen **Config‑Flow**, es ist keine YAML‑Konfiguration notwendig.

Nach der Einrichtung erscheint ein Sensor:

sensor.nrw_rail_status_sensor
---

## 🧠 Sensor‑Daten

### **State**
- Anzahl der aktiven Störungen

### **Attribute**
- `first_title` – Titel der ersten Meldung  
- `first_text` – Beschreibung (Markdown)  
- `first_start` – Startzeitpunkt  
- `first_end` – Endzeitpunkt  
- `first_priority` – Priorität  
- `first_comp` – Verbund (z. B. VRR, NWL)  
- `first_product` – Produktklasse  
- `first_id` – Meldungs‑ID  
- `messages` – Liste aller Meldungen als strukturierte Objekte

---

## 📊 Beispiel‑Dashboard (Standard‑HA‑Karten)

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
      {% set s = states('sensor.nrw_rail_status_sensor') | int %}
      {% set first = state_attr('sensor.nrw_rail_status_sensor', 'messages')[0] if s > 0 else None %}

      **Aktuelle Störungen:** {{ s }}

      {% if s > 0 %}
      **Titel:** {{ first.title }}

      **Beschreibung:**  
      {{ first.text }}

      **Beginn:** {{ first.start }}  
      **Ende:** {{ first.end }}

      **Priorität:** {{ first.priority }}  
      **Verbund:** {{ first.comp }}  
      **Produkt:** {{ first.product }}  
      **Meldungs-ID:** {{ first.id }}
      {% else %}
      Keine aktuellen Störungen gemeldet.
      {% endif %}

  - type: markdown
    title: Alle Störungen
    content: |
      {% set msgs = state_attr('sensor.nrw_rail_status_sensor', 'messages') %}
      {% if msgs %}
      {% for m in msgs %}
      ---
      ### **{{ m.title }}**
      **Beschreibung:**  
      {{ m.text }}

      **Beginn:** {{ m.start }}  
      **Ende:** {{ m.end }}

      **Priorität:** {{ m.priority }}  
      **Verbund:** {{ m.comp }}  
      **Produkt:** {{ m.product }}  
      **ID:** {{ m.id }}

      {% endfor %}
      {% else %}
      Keine Störungen vorhanden.
      {% endif %}
