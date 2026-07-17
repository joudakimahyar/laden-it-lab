# SCHRITT 2 – Artikelverwaltung, Tagesbericht und Kassenbon

**Ziel:** Drei neue Funktionen zur Kasse hinzufügen: Artikelverwaltung, Tagesbericht und PDF-Kassenbon.

**Gebaut:**
- Neue Seite /artikel zur Verwaltung der Artikel (anlegen, bearbeiten, löschen) mit voller CRUD-Funktionalität über die API.
- Neue Seite /bericht mit Tagesbericht (Anzahl Verkäufe, Umsatz) und Datumsauswahl für vergangene Tage.
- Automatische PDF-Kassenbon-Erstellung nach jedem Verkauf (Datum, Artikel, Summe) im A6-Format.

**Screenshot/Demo:** (ich ergänze das später)

**Architektur:** Browser --> Kassen-App (FastAPI) --> Datenbank (SQLite), mit neuen Endpunkten für Artikel-CRUD, Tagesbericht und PDF-Generierung.

**Gelernt:** CRUD-Prinzip (Create, Read, Update, Delete), warum Verkäufe ihre eigenen Artikel-Daten als Snapshot speichern statt live zu verlinken, Arbeiten mit PDF-Bibliotheken (fpdf2), Umgang mit Encoding-Problemen (Euro-Zeichen), UTC vs. lokale Zeit bei Datumsfiltern.

**Problem & Lösung:** Beim Testen traten mehrere Probleme auf: (1) "A6" wurde von fpdf2 nicht als Format-String erkannt, gelöst durch explizite Maßangabe (105x148mm). (2) Das Euro-Zeichen wurde von der Standard-Schrift nicht unterstützt, gelöst durch Ersetzen mit "EUR" im PDF. (3) Ein pkill-Befehl unterbrach eine Befehlskette, wodurch der Server nicht neu startete - gelöst durch Aufteilen in separate Schritte. Jedes Problem wurde durch Live-Tests entdeckt, nicht nur durch Code-Review.

**Nächster Schritt:** Schritt 3 – Die Kasse auf einen echten Linux-Server bringen.
