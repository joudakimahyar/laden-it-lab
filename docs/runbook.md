# Runbook

Dieses Runbook beschreibt zwei wiederkehrende Aufgaben im laden-it-lab-Projekt,
Schritt für Schritt und so, dass sie auch ohne viel Vorwissen nachvollziehbar
sind: das Einrichten eines neuen Kassen-Arbeitsplatzes und das Zurückspielen
eines Datenbank-Backups im Notfall.

## a) Neue Kasse einrichten

Ziel: Ein neuer Windows-Client soll als Kassen-Arbeitsplatz im Laden-Netzwerk
funktionieren — mit Domain-Login, einem Klick auf die Kasse und ohne dass der
Kassierer versehentlich Admin-Rechte hat.

### 1. Windows-Client in die Domäne aufnehmen

1. Windows-Client mit dem Labor-Netzwerk verbinden (Internal Network
   `labornetz` in VirtualBox, statische IP oder DHCP — Hauptsache er kann den
   Windows Server unter `192.168.56.10` per DNS erreichen).
2. Als lokaler Administrator einloggen und in PowerShell prüfen, ob der
   Domain Controller erreichbar ist:
   ```powershell
   nslookup laden.local
   ```
3. Client der Domäne hinzufügen:
   ```powershell
   Add-Computer -DomainName "laden.local" -Restart
   ```
4. Nach dem Neustart erscheint bei der Anmeldung die Domäne `LADEN`. Mit
   einem AD-Benutzer (z. B. `sara`) einloggen, um den Domain-Join zu
   bestätigen.

### 2. Browser-Verknüpfung zur Kasse anlegen

1. Auf dem Desktop des Kassen-Arbeitsplatzes Rechtsklick →
   **Neu → Verknüpfung**.
2. Als Ziel eintragen:
   ```
   http://kasse.laden.local:8000
   ```
3. Verknüpfung benennen, z. B. "Kasse", und optional ein passendes Icon
   vergeben.
4. Testen: Doppelklick auf die Verknüpfung öffnet den Standardbrowser direkt
   auf der Kassen-Startseite. Falls das nicht klappt, prüfen, ob der
   DNS-A-Record für `kasse` auf dem Windows Server existiert und auf die
   richtige IP des Ubuntu-Servers zeigt (siehe Woche 8, Problem & Lösung).

### 3. Eingeschränkten Benutzer erstellen

Der Kassierer soll die Kasse bedienen können, aber keine Admin-Aktionen auf
dem Windows-Client ausführen können (Prinzip der minimalen Rechte /
Least Privilege).

1. Lokalen Benutzer anlegen (in einer PowerShell **als Administrator**):
   ```powershell
   net user kassierer <Passwort> /add
   ```
2. Sicherstellen, dass der Benutzer **nur** in der Gruppe "Users" ist und
   **nicht** in "Administrators":
   ```powershell
   net user kassierer
   ```
   Die Ausgabe sollte unter "Local Group Memberships" nur `*Users` zeigen.
3. Mit dem Benutzer `kassierer` einloggen und die Browser-Verknüpfung zur
   Kasse auf dessen Desktop anlegen (siehe Schritt 2).
4. Test der Rechte-Einschränkung: Eine Admin-Aktion auslösen (z. B. eine neue
   Software installieren oder die Systemzeit ändern). Windows muss dabei per
   User Account Control (UAC) ein Administrator-Passwort verlangen — meldet
   sich stattdessen sofort eine Aktion ohne Nachfrage aus, ist der Benutzer
   fälschlicherweise Mitglied der Administratoren-Gruppe.

## b) Backup zurückspielen

Ziel: Die Kassen-Datenbank (`kasse.db`) im Notfall aus einem der
automatisch erstellten Backups wiederherstellen (Backups werden laut Woche 7
täglich per Cron-Job in `/home/mahyar/laden-it-lab/backups/` abgelegt, siehe
`backup.sh`).

1. Auf dem Ubuntu-Server (`kasse-server`) per SSH einloggen und verfügbare
   Backups auflisten:
   ```bash
   ls -lt /home/mahyar/laden-it-lab/backups/
   ```
   Die Dateien sind nach Zeitstempel benannt, z. B.
   `kasse_2026-07-15_18-26-41.db`. Das gewünschte Backup auswählen (meist
   das neueste, außer man will gezielt einen älteren Stand wiederherstellen).
2. Den Kassen-Dienst stoppen, damit die Datenbank während des
   Zurückspielens nicht beschrieben wird:
   ```bash
   sudo systemctl stop kasse
   ```
3. Die aktuelle (evtl. beschädigte) Datenbank zur Sicherheit beiseite legen,
   statt sie direkt zu löschen:
   ```bash
   mv /home/mahyar/laden-it-lab/kasse.db /home/mahyar/laden-it-lab/kasse.db.beschaedigt
   ```
4. Das gewählte Backup als neue `kasse.db` einspielen:
   ```bash
   cp /home/mahyar/laden-it-lab/backups/kasse_<ZEITSTEMPEL>.db /home/mahyar/laden-it-lab/kasse.db
   ```
5. Kassen-Dienst wieder starten und Status prüfen:
   ```bash
   sudo systemctl start kasse
   sudo systemctl status kasse
   ```
6. Im Browser (`http://kasse.laden.local:8000`) prüfen, ob die
   wiederhergestellten Daten (Artikel, Verkäufe) wie erwartet vorhanden sind.

**Hinweis:** Dieser Ablauf wurde bereits in Woche 7 als Restore-Test
durchgeführt (Datenbank absichtlich beschädigt und erfolgreich aus einem
Backup wiederhergestellt) — dieses Runbook beschreibt genau diesen Ablauf
für den echten Ernstfall.
