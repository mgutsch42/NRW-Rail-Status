# NRW Rail Status – Home Assistant Integration

## ⚠️ Aktueller Status

Die bisherige Datenquelle (**Zuginfo.nrw / HIM‑API**) liefert seit einer API‑Änderung **keine stabilen oder vollständigen Daten** mehr.  
Die Integration funktioniert technisch, aber die API liefert:

- HAMM‑Fehler  
- leere oder unvollständige JSON‑Antworten  
- abweichende Strukturen gegenüber bekannten HAFAS/HIM‑Implementierungen  

Das Projekt befindet sich daher aktuell in einer **Analyse‑ und Übergangsphase**.

👉 Aktueller Stand & Diskussion:  
https://github.com/mgutsch42/nrw-rail-status/issues/2

---

## 🤝 Hinweis für Contributor

Dieses Projekt ist ein Community‑Projekt.  
Ich selbst bin **kein Experte für HAFAS/HIM‑APIs oder Reverse‑Engineering** und lerne vieles gerade erst kennen.

Ich kann:

- das Projekt koordinieren  
- testen  
- dokumentieren  
- die Integration weiterentwickeln  

Aber ich bin auf **fachliche Unterstützung bei der API‑Analyse** angewiesen.

**Kurz gesagt:**  
Ich bringe Struktur, Motivation und die Integration selbst mit —  
die Community bringt das API‑Know‑how mit.

Jede Hilfe ist willkommen: Hinweise, Tests, Logs, Code.

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

