# NRW Rail Status (Home Assistant Integration)

Diese Home‑Assistant‑Integration zeigt **aktuelle Störungen, Baustellen und Meldungen** aus dem nordrhein‑westfälischen Bahnnetz an.  
Die Daten stammen direkt aus **Zuginfo.nrw** und werden über die offizielle **HAFAS‑HIM‑Schnittstelle** abgerufen.

Die Integration ist vollständig lokal, benötigt keine Cloud‑Dienste und funktioniert ohne API‑Key.

---

## ✨ Features

- Echtzeit‑Abruf der NRW‑HIM‑Meldungen (Störungen, Baustellen, Ausfälle)
- Auflösung aller HAFAS‑Referenzen:
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

