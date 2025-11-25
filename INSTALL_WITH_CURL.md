# 🚀 Schnelle Installation mit curl

Die **einfachste und schnellste Methode** zur Installation auf dem Raspberry Pi!

## One-Liner Installation

```bash
curl -fsSL https://raw.githubusercontent.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/main/install_rest_api.sh | bash
```

## Was macht das Skript?

✅ **Automatische Konfiguration:**
- Prüft Python & git Installation
- Lädt Projekt von GitHub herunter
- Installiert nur **core dependencies** (kein PyQt6!)
  - `flask`, `flask-cors`, `pyyaml`, `requests`
- Erstellt `config.yaml` mit deinen Credentials
- Richtet Systemd Service ein (optional, mit Autostart)
- Verifiziert Installation

✅ **Praktische Features:**
- Fehlerbehandlung (Exit bei Fehlern)
- Interaktive Credential-Eingabe
- Optional: Systemd Service für Autostart
- Logs & Debugging
- Health-Check nach Installation

**Wichtig:** PyQt6 (GUI) wird NICHT installiert!
- REST API braucht nur core Dependencies
- PyQt6 würde lange Kompilierung auf Raspi brauchen
- Für Desktop GUI: `pip install -r requirements-gui.txt`

## Schritt-für-Schritt

### 1. SSH auf Raspi verbinden
```bash
ssh root@192.168.1.100
```

### 2. Installation starten
```bash
curl -fsSL https://raw.githubusercontent.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/main/install_rest_api.sh | bash
```

### 3. Fragen beantworten
- Tuya Access ID
- Tuya Access Key  
- Tuya Device ID
- Region (eu/us/cn) - Default: eu
- Systemd Service installieren? (j/n)

### 4. Fertig! 🎉
Die REST API läuft unter `http://192.168.1.100:5000`

## Alternativen

Wenn curl nicht funktioniert:

```bash
# Mit wget
wget -qO- https://raw.githubusercontent.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/main/install_rest_api.sh | bash

# Oder manuelle Installation (siehe HOMEASSISTANT_QUICKSTART.md)
```

## Was nach der Installation?

1. ✅ REST API läuft als Systemd Service (bei Option "j")
2. ✅ config.yaml ist erstellt
3. ✅ Dependencies sind installiert

### Home Assistant konfigurieren

In `configuration.yaml`:
```yaml
rest_command:
  tuya_get_properties:
    url: "http://192.168.1.100:5000/properties"
    method: get
  
  tuya_set_property:
    url: "http://192.168.1.100:5000/set"
    method: post
    payload: '{"property":"{{ property }}", "value":{{ value }}}'
    content_type: application/json
```

## Troubleshooting

**Problem: curl nicht gefunden**
```bash
apt-get update && apt-get install curl -y
```

**Problem: Git-Klonen fehlgeschlagen**
- Überprüfe SSH-Key oder PAT (Personal Access Token)
- Alternative: Mit scp manuell kopieren

**Problem: API startet nicht**
```bash
# Status prüfen
systemctl status tuya-api

# Logs anschauen
journalctl -u tuya-api -f

# Manuell starten zum Debuggen
cd /root/tuya_client
python3 src/tuya_homeassistant_api.py --port 5000
```

## Weitere Dokumentation

- 📖 [HOMEASSISTANT_QUICKSTART.md](./docs/HOMEASSISTANT_QUICKSTART.md) - Komplette Setup-Anleitung
- 📖 [HOMEASSISTANT_COMPLETE.md](./docs/HOMEASSISTANT_COMPLETE.md) - Umfassende Referenz
- 📖 [HOMEASSISTANT_EXAMPLES.md](./docs/HOMEASSISTANT_EXAMPLES.md) - Automationen & Beispiele

---

**Fragen?** → GitHub Issues: https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/issues
