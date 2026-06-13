# NRW-Rail-Status

**⚠️ Hinweis:**  
Dieses Projekt befindet sich aktuell in aktiver Entwicklung.  
Funktionen, Struktur und API‑Verhalten können sich noch ändern.  
Die Integration ist derzeit vor allem für Tests und frühe Anwender gedacht.

---

`nrw‑rail‑status` ist eine Home‑Assistant‑Integration, die aktuelle Einschränkungen im Regionalverkehr Nordrhein‑Westfalen übersichtlich darstellt.  
Die Integration sammelt und verarbeitet Informationen zu:

- **Störungen** (z. B. Signalstörungen, Weichenstörungen, Fahrzeugdefekte)
- **Bauarbeiten** (geplante und laufende Maßnahmen)
- **Sperrungen und Umleitungen**
- **betriebliche Einschränkungen** auf einzelnen Strecken oder Linien

Damit bietet die Integration eine zentrale Übersicht über die Verkehrslage im NRW‑Regionalverkehr und ermöglicht es, diese Informationen in **Dashboards**, **Automationen** und **Benachrichtigungen** einzubinden.

Die Daten stammen aus öffentlich zugänglichen Quellen von **Zuginfo.nrw**.  
Dieses Projekt steht in **keiner Verbindung** zu Zuginfo.nrw, dem VRR oder der Deutschen Bahn.

---

## Installation & Neustart

Nach der Installation oder Aktualisierung dieser Integration über HACS muss  
Home Assistant **neu gestartet** werden.  
Dies ist notwendig, weil Home Assistant den Ordner `custom_components` nur beim Start einliest und neue oder geänderte Integrationen erst dann aktiv werden.

### Schritte zur Installation

1. HACS → Integrationen → *Custom repositories*
2. Repository-URL: `https://github.com/mgutsch42/nrw-rail-status`
3. Typ: *Integration*
4. Integration installieren
5. **Home Assistant neu starten**
6. Integration unter *Einstellungen → Geräte & Dienste* hinzufügen

Ohne den Neustart erscheint die Integration nicht im Home‑Assistant‑Frontend.

---

## Aktueller Funktionsumfang

- Sensor für Anzahl der aktuellen Störungen
- Basis‑API‑Abfrage
- Attribute für Linie, Kategorie, Beschreibung, Start/Ende, letzte Aktualisierung

---

## Geplante Funktionen (Roadmap)

- [ ] Erweiterte Sensorstruktur (mehrere Störungen gleichzeitig)
- [ ] Lovelace‑Tabellenansicht
- [ ] Filteroptionen (Linien, Regionen, Kategorien)
- [ ] Verbesserte Fehlerbehandlung
- [ ] Vorbereitung eines offiziellen HACS‑Releases

3. Typ: *Integration*  
4. Installieren und Home Assistant neu starten  
