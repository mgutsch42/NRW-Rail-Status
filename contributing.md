# Contributing Guide – NRW Rail Status

Vielen Dank für dein Interesse an der Weiterentwicklung dieser Home‑Assistant‑Integration!  
Da die ursprüngliche API von Zuginfo.nrw nicht mehr verfügbar ist, suchen wir gemeinsam nach
neuen Datenquellen und arbeiten an einer stabilen Nachfolgeversion.

Beiträge jeder Art sind willkommen – egal ob Code, Recherche, Tests oder Ideen.

---

## 🚀 Wie du beitragen kannst

### Issues erstellen
Nutze Issues für:

- Vorschläge zu neuen APIs oder Datenquellen  
- Bugreports  
- Ideen für neue Funktionen  
- Fragen zur Entwicklung  

Bitte beschreibe dein Anliegen so klar wie möglich.

---

### Pull Requests (PRs)
Wenn du Code beitragen möchtest:

1. Repository forken  
2. Neuen Branch erstellen  
3. Änderungen implementieren  
4. Lokal testen  
5. Pull Request öffnen

Bitte achte darauf:

- klare Commit‑Nachrichten  
- kleine, gut nachvollziehbare Änderungen  
- Beschreibung im PR, was du geändert hast und warum  

---

## 🔍 Fokus der aktuellen Entwicklung

Da die ursprüngliche API nicht mehr existiert, suchen wir aktiv nach Alternativen:

- DB Transport REST API (transport.rest)  
- NRW OpenData  
- GTFS‑RT‑Feeds  
- mögliche neue Endpunkte von Zuginfo.nrw  
- andere öffentliche Quellen für Störungs‑ und Betriebsinformationen  

Wenn du eine API findest, die geeignet sein könnte, eröffne bitte ein Issue oder PR.

---

## 🛠️ Lokale Entwicklung

### Voraussetzungen
- Python 3.11+  
- Home Assistant Core oder Home Assistant OS mit `custom_components`‑Ordner  
- Git

### Integration lokal testen
1. Repository klonen  
2. Ordner `custom_components/nrw_rail_status` in dein Home‑Assistant‑Verzeichnis kopieren  
3. Home Assistant neu starten  
4. Integration hinzufügen

---

## 📐 Code‑Richtlinien

- Halte dich an die Home‑Assistant‑Entwicklerstandards  
- Nutze Typannotationen  
- Schreibe klaren, gut lesbaren Code  
- Füge Logging hinzu, wo sinnvoll  
- Vermeide unnötige Abhängigkeiten

---

## 💬 Kommunikation

Du kannst dich beteiligen über:

- Issues  
- Pull Requests  
- Discussions (falls aktiviert)  

Alle Beiträge sind willkommen – egal ob klein oder groß.

---

## ❤️ Danke!

Open‑Source lebt von Menschen wie dir.  
Danke, dass du dazu beiträgst, diese Integration weiterzuentwickeln!
