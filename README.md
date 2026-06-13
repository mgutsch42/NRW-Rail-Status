# NRW Rail Status – Home Assistant Integration

Diese Home‑Assistant‑Integration zeigt aktuelle Störungen und Meldungen aus dem NRW‑Bahnnetz an.  
Die Daten stammen von der öffentlichen API von **Zuginfo.nrw**.

> **Hinweis: Diese Integration befindet sich aktuell in aktiver Entwicklung / Testphase.**  
> Funktionen können sich ändern, es können Fehler auftreten und nicht alle Datenpunkte sind final.  
> Rückmeldungen und Fehlerberichte sind ausdrücklich erwünscht.

---

## 🚆 Funktionsumfang

- Abfrage der öffentlichen RIS‑API von https://www.zuginfo.nrw/api/ris  
- Automatische Aktualisierung alle 60 Sekunden  
- Sensor zeigt:
  - **State:** Anzahl der aktuellen Störungen
  - **Attribute:** Details zur *ersten* Störung
  - **raw:** komplette JSON‑Liste aller Störungen (für Dashboards)

---

## 📦 Installation über HACS

1. HACS → **Integrationen**
2. Rechts oben: **Custom repositories**
3. URL eintragen:

