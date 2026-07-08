# laden-it-lab

Ein kleines Kassensystem (Point-of-Sale) als Lernprojekt im Rahmen der Ausbildung
zum Fachinformatiker Systemintegration.

## Architektur

```mermaid
graph LR
    A[Browser] -->|Artikel, Verkauf, Bericht| B[Kassen-App - FastAPI]
    B --> C[(Datenbank - SQLite)]
    B -->|nach Verkauf| D[PDF-Kassenbon - fpdf2]
    D -->|Download| A
```

## Fortschritt

- [Woche 1 – Die Kasse läuft](docs/woche-01.md)
- [Woche 2 – Artikelverwaltung, Tagesbericht und Kassenbon](docs/woche-02.md)
