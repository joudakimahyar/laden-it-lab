# WOCHE 6 – Windows Server & Active Directory

**Ziel:** Eine zentrale Benutzerverwaltung mit Active Directory einrichten, sodass ein Kassierer-Konto von einem separaten Client-PC aus einloggen kann.

**Gebaut:**
- Windows Server 2025 (Evaluation) als VM installiert und zum Domain Controller für die Domäne `laden.local` befördert (Install-ADDSForest)
- Sicherheitsgruppe "Kassierer" und Benutzer "sara" per PowerShell (New-ADGroup, New-ADUser) erstellt und der Gruppe zugewiesen
- Windows 11 Enterprise (Evaluation) als zweite VM ("win-client") installiert
- Beide VMs auf ein gemeinsames VirtualBox Internal Network (`labornetz`) umgestellt, mit statischen IPs (Server: 192.168.56.10, Client: 192.168.56.20) und DNS-Konfiguration auf den Server
- Client erfolgreich der Domäne `laden.local` hinzugefügt (Add-Computer)
- Erfolgreicher Login als `LADEN\sara` auf dem Client-PC, inkl. erzwungener Passwortänderung beim ersten Login

**Screenshot/Demo:** siehe bilder/woche6-vm-details.png, bilder/woche6-server-ip-config.png, bilder/woche6-server-dns-verify.png, bilder/woche6-dns-test.png, bilder/woche6-domain-join.png, bilder/woche6-sara-login.png

**Architektur:** siehe aktualisiertes Diagramm im README (Server, Client und AD als neue Bausteine)

**Gelernt:**
- Active Directory Grundlagen: Domain Controller, Domäne, Sicherheitsgruppen, Benutzerverwaltung
- Windows Server Core (ohne GUI) über PowerShell und SConfig bedienen
- VirtualBox-Netzwerktypen (NAT vs. Internal Network) und wann man welchen braucht
- Statische IP-Konfiguration und DNS-Client-Einstellungen unter Windows

**Problem & Lösung:**
Windows Server war als Server Core (ohne Desktop) installiert, daher gab es keinen Explorer und keine grafische Oberfläche für Shared Clipboard/Guest Additions. Alle Konfigurationsschritte (IP, DNS, AD, Domain-Join) wurden stattdessen komplett über PowerShell erledigt. Zusätzlich sorgte die deutsche Tastaturbelegung in der VM für vertippte Sonderzeichen (z. B. `$` wurde zu `§`, `_` zu `-`); Lösung war, Befehle möglichst ohne Sonderzeichen zu schreiben und Tippfehler genau zu prüfen.

**Nächster Schritt:** Woche 7 – Backup der Kassendatenbank automatisieren und ein einfaches Monitoring (Uptime Kuma) einrichten.
