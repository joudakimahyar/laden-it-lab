# WOCHE 1 – Die Kasse läuft

**Ziel:** Eine einfache Kasse bauen, die im Browser läuft: Artikel wählen, Summe sehen, Verkauf abschließen.

**Gebaut:** FastAPI-Anwendung mit 5 Beispiel-Artikeln, Warenkorb-Funktion, Speicherung der Verkäufe in SQLite.

**Screenshot/Demo:** siehe [bilder/woche1-kasse.png](../bilder/woche1-kasse.png)

**Architektur:** Browser --> Kassen-App (FastAPI) --> Datenbank (SQLite)

**Gelernt:** Grundlagen von FastAPI und Python, wie Web-Anwendungen mit einer Datenbank zusammenarbeiten, Git/GitHub Workflow, SSH-Key und ssh-agent.

**Problem & Lösung:** Beim Verbinden mit GitHub kam die Fehlermeldung "Permission denied (publickey)". Der Grund war, dass der SSH-Agent nicht lief. Lösung: mit `eval "$(ssh-agent -s)"` den Agent gestartet und mit `ssh-add ~/.ssh/id_ed25519` meinen Schlüssel hinzugefügt.

**Nächster Schritt:** Woche 2 – Artikelverwaltung, Kassenbon und Tagesbericht.
