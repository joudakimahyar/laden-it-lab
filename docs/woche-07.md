# WOCHE 7 – Backup & Monitoring

**Ziel:** Ein automatisches tägliches Backup der Kassen-Datenbank einrichten und mit Uptime Kuma ein einfaches Monitoring für die Kasse aufsetzen.

**Gebaut:**
- Backup-Skript (`backup.sh`) geschrieben: kopiert `kasse.db` mit Zeitstempel in einen `backups/`-Ordner
- Mit `crontab` eingerichtet, dass das Skript jede Nacht um 2:00 Uhr automatisch läuft
- Restore-Test durchgeführt: eine Kopie der Datenbank absichtlich "beschädigt" und erfolgreich aus einem Backup wiederhergestellt
- Uptime Kuma per Docker installiert und einen Monitor für die Kassen-App (`http://localhost:8000`) eingerichtet
- Port Forwarding in VirtualBox für Port 3001 (Uptime Kuma) hinzugefügt

**Screenshot/Demo:** siehe bilder/woche7-backup-script.png, bilder/woche7-cron-setup.png, bilder/woche7-uptimekuma-install.png, bilder/woche7-port-forwarding.png, bilder/woche7-monitoring-success.png

**Architektur:** siehe aktualisiertes Diagramm im README (Backup-Ordner und Monitoring als neue Bausteine)

**Gelernt:**
- Bash-Skripte schreiben (Variablen, Zeitstempel, Dateioperationen)
- Automatisierung mit cron (Zeitsyntax: Minute, Stunde, Tag, Monat, Wochentag)
- Backup- und Restore-Prinzip in der Praxis testen, nicht nur einrichten
- Docker-Grundlagen: Container starten, stoppen, entfernen, Netzwerktypen (Bridge vs. Host)
- Zusammenspiel von Firewall (UFW), Docker-Netzwerken und VirtualBox Port Forwarding

**Problem & Lösung:**
Nach der Installation von Uptime Kuma zeigte der Monitor für die Kassen-App dauerhaft "Down" mit dem Fehler `ECONNREFUSED`. Die Fehlersuche zeigte mehrere Ursachen: Erstens lief Uptime Kuma zunächst in einem isolierten Docker-Netzwerk und konnte den Kassen-Service auf demselben Server nicht erreichen – das wurde durch einen Neustart des Containers mit `--network=host` gelöst. Zweitens blockierte die zuvor in Woche 4 eingerichtete Firewall (UFW) den Port 3001 von außen, obwohl der Dienst intern einwandfrei lief (bestätigt durch `curl http://localhost:3001` direkt auf dem Server). Die Lösung war, den Port explizit mit `sudo ufw allow 3001/tcp` freizugeben. Diese zweistufige Fehlersuche (erst Docker-Netzwerk, dann Firewall) hat gezeigt, wie wichtig es ist, Schicht für Schicht zu prüfen: zuerst intern (Service selbst), dann lokal (Container-Netzwerk), dann extern (Firewall und Port Forwarding).

**Nächster Schritt:** Woche 8 – Windows-Client als Kassen-Arbeitsplatz einrichten, Runbook schreiben und das Projekt für GitHub abschließend dokumentieren.
