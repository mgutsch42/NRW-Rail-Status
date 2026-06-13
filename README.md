# NRW Rail Status – Home Assistant Integration

Die **NRW Rail Status** Integration stellt aktuelle Störungsmeldungen des Schienenverkehrs in Nordrhein‑Westfalen bereit.  
Sie eignet sich für Pendler, ÖPNV‑Nutzer und alle, die Störungen im Bahnverkehr automatisiert überwachen möchten.

Die Integration ruft die Daten von **Zuginfo.nrw** ab und bereitet sie für Home Assistant auf.  
Dieses Projekt steht in **keiner Verbindung** zu Zuginfo.nrw, dem VRR oder der Deutschen Bahn.

---

## 🚧 Entwicklungsstatus

Diese Integration befindet sich **aktuell in aktiver Entwicklung**.  
Funktionen, Struktur und API‑Verhalten können sich jederzeit ändern.

**Derzeitiger Stand:**

- Sensor für Anzahl der aktuellen Störungen
- API‑Abruf implementiert
- Attribute pro Störung verfügbar
- Automatische Aktualisierung über DataUpdateCoordinator

---

## ✨ Funktionsumfang

- Anzeige der **Anzahl aktueller Störungen**
- Abruf der offiziellen NRW‑Störungsmeldungen
- Sensorattribute pro Störung:
  - Linie
  - Kategorie
  - Beschreibung
  - Startzeit
  - Endzeit
  - Letzte Aktualisierung
- Integration in Dashboards, Automationen und Benachrichtigungen

---

## 📦 Installation über HACS

### 1. Custom Repository hinzufügen  

https://github.com/mgutsch42/nrw-rail-status


Typ: **Integration**

### 2. Integration installieren  
Nach dem Hinzufügen erscheint die Integration in HACS und kann installiert werden.

### 3. Home Assistant neu starten

---

## 🛠 Manuelle Installation

Falls du die Integration ohne HACS installieren möchtest:

1. Ordner erstellen:

/config/custom_components/nrw_rail_status/


2. Alle Dateien aus diesem Repository in diesen Ordner kopieren  
3. Home Assistant neu starten

---

## 🧩 Sensor

Nach der Installation steht ein Sensor zur Verfügung:

sensor.nrw_rail_status


### Sensorattribute:

- `line`
- `category`
- `description`
- `start_time`
- `end_time`
- `last_update`

---

## 🗺 Beispiel Lovelace‑Karte

```yaml
type: entities
title: NRW Rail Status
entities:
  - entity: sensor.nrw_rail_status

HACS → Integrationen → Custom repositories

