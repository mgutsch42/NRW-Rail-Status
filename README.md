# NRW Rail Status – Home Assistant Integration

## ⚠️ Aktueller Status

Die bisherige Datenquelle (Zuginfo.nrw / HIM‑API) liefert seit einer API‑Änderung keine stabilen oder vollständigen Daten mehr.  
Die Integration funktioniert technisch, aber die API liefert:

- HAMM‑Fehler
- leere oder unvollständige JSON‑Antworten
- abweichende Strukturen gegenüber bekannten HAFAS/HIM‑Implementierungen

Das Projekt befindet sich daher aktuell in einer Analyse‑ und Übergangsphase.

Aktueller Stand & Diskussion:  
https://github.com/mgutsch42/nrw-rail-status/issues/2

---

## 🤝 Hinweis für Contributor

Dieses Projekt ist ein Community‑Projekt.  
Ich selbst bin kein Experte für HAFAS/HIM‑APIs oder Reverse‑Engineering und lerne vieles gerade erst kennen.

Ich kann:

- das Projekt koordinieren
- testen
- dokumentieren
- die Integration weiterentwickeln

Aber ich bin auf fachliche Unterstützung bei der API‑Analyse angewiesen.

Kurz gesagt:  
Ich bringe Struktur, Motivation und die Integration selbst mit —  
die Community bringt das API‑Know‑how mit.

Jede Hilfe ist willkommen: Hinweise, Tests, Logs, Code.

---

## 🚆 Funktionsumfang

Hinweis: Die folgenden Funktionen sind aktuell nur eingeschränkt nutzbar, da die API keine verwertbaren Daten liefert.

- Live‑Abruf der NRW‑HIM‑API (HimSearch)
- Anzeige der aktuellen Anzahl von Störungen
- Detailinformationen zur ersten Störung
- Vollständige Liste aller Meldungen (Titel, Text, Zeitraum, Priorität, Verbund)
- Automatische Aktualisierung über einen Update‑Coordinator
- Kompatibel mit Standard‑Home‑Assistant‑Karten

---

## 📦 Installation über HACS (manuell)

1. HACS → Integrationen
2. Rechts oben: Custom repositories
3. Folgende URL eintragen:

   https://github.com/mgutsch42/nrw-rail-status

4. Typ: Integration
5. Repository hinzufügen
6. Integration installieren
7. Home Assistant neu starten
8. Integration hinzufügen: NRW Rail Status

---

## ⚙️ Konfiguration

Die Integration nutzt einen Config‑Flow, es ist keine YAML‑Konfiguration notwendig.

Nach der Einrichtung erscheint ein Sensor:

sensor.nrw_rail_status_sensor

---

## 🧠 Sensor‑Daten

State:
- Anzahl der aktiven Störungen

Attribute:
- first_title – Titel der ersten Meldung
- first_text – Beschreibung (Markdown)
- first_start – Startzeitpunkt
- first_end – Endzeitpunkt
- first_priority – Priorität
- first_comp – Verbund (z. B. VRR, NWL)
- first_product – Produktklasse
- first_id – Meldungs‑ID
- messages – Liste aller Meldungen als strukturierte Objekte

---

## 📊 Beispiel‑Dashboard (ohne YAML‑Block)

Hinweis: YAML‑Beispiel wurde entfernt, damit der Markdown‑Block nicht zerstört wird.  
Du kannst es später wieder einfügen, wenn du möchtest.

---

## 🧩 Technische Details

Die Integration basiert auf:

- Config Flow — UI‑basierte Einrichtung
- DataUpdateCoordinator — zyklische API‑Abfrage
- Sensor‑Plattform — strukturierte Attribute
- Logging — Debug‑Ausgaben
- Asynchronem HTTP‑Client (aiohttp)

Die Integration ist technisch stabil, aber die Datenquelle liefert aktuell keine verwertbaren Antworten.  
Die bisherigen API‑Endpunkte der NRW‑RIS‑Seite scheinen ersetzt oder abgeschaltet worden zu sein.  
Die neue HIM‑API liefert:

- HAMM‑Fehler
- leere oder unvollständige JSON‑Antworten
- abweichende Strukturen gegenüber bekannten HAFAS/HIM‑Implementierungen

Die Integration erwartet ein konsistentes JSON‑Format, das derzeit nicht geliefert wird.

---

## 🧪 Was bereits getestet wurde

Folgende Tests wurden bereits durchgeführt:

- direkte API‑Abfragen über Browser, Postman und aiohttp
- GET‑ und POST‑Varianten der HIM‑Endpunkte
- Parameter wie format=json, limit, filter
- Analyse der Netzwerk‑Requests der NRW‑Webseite (XHR‑Calls)
- Vergleich mit bekannten HAFAS/HIM‑Implementierungen anderer Verkehrsverbünde
- Test der Integration in Home Assistant (Config‑Flow, Coordinator, Sensor)
- Debug‑Logging der vollständigen API‑Antworten
- Prüfung alternativer Datenquellen (VRR, NVR, NWL, DB, GTFS‑RT)
- Validierung der JSON‑Struktur gegen erwartete HAFAS/HIM‑Schemas

Ergebnis:  
Die API liefert derzeit keine stabile, verwertbare Struktur.  
Daher ist API‑Analyse und Reverse‑Engineering aktuell der wichtigste Schritt.

---

## 📄 Lizenz

Wird später ergänzt.


