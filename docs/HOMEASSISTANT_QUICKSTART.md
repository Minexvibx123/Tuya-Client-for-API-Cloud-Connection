# Home Assistant Integration - Schnellstart

## 🚀 5-Minuten Setup

### Option 1: PyScript (Empfohlen - Vollständig)

**1. PyScript Installation & Dependencies**

```
Home Assistant → Einstellungen → Zusatzprogramme → HACS
```

a) HACS öffnen (falls nicht installiert):
```
Instellungen → Geräte & Dienste → HACS
(oder https://www.hacs.xyz/ für Installation)
```

b) PyScript suchen & installieren:
```
HACS → Automation (Suchfeld oben)
Suche: "PyScript"
Klick auf "pyscript"
Klick: "INSTALL"
```

c) Home Assistant neu starten
```
Einstellungen → System → Starten Sie Home Assistant neu
oder
Terminal: systemctl restart homeassistant
```

d) PyScript aktivieren in `configuration.yaml`:
```yaml
pyscript:
  allow_all_imports: true
  file_reloader: true
```

e) Nochmal neu starten

**2. Dependencies in PyScript installieren**

PyScript lädt diese automatisch herunter (wenn erlaubt):
- `requests` - HTTP-Requests zu Tuya API
- `yaml` - Config-Dateien lesen
- `hmac` - Signierung (im Python Standard)
- `hashlib` - Hashing (im Python Standard)
- `json` - JSON-Verarbeitung (im Python Standard)
- `time` - Zeit-Funktionen (im Python Standard)
- `logging` - Logging (im Python Standard)

*Die meisten sind bereits in Python enthalten!*

Wenn du manuell installieren musst:

```bash
# SSH in Home Assistant oder Terminal Add-on
pip install requests pyyaml

# oder für Home Assistant Container:
docker exec homeassistant pip install requests pyyaml
```

**3. Datei erstellen**
```
/config/pyscript/tuya_client.py
```
Kopiere Inhalt aus `docs/HOMEASSISTANT_COMPLETE.md` (tuya_client.py Sektion)

**4. Credentials eintragen**
```python
TUYA_ACCESS_ID = "xxxxx"
TUYA_ACCESS_KEY = "xxxxx"
TUYA_DEVICE_ID = "xxxxx"
```

**5. Home Assistant neu starten**

**6. Lovelace Dashboard nutzen**
```yaml
- entity: input_boolean.tuya_power
  name: "Power"
```

---

### Detaillierte Anleitung: Wie PyScript Dependencies herunterlädt

#### Schritt 1: HACS Installation
```
1. Gehe zu: Home Assistant → Einstellungen
2. Wähle: "Geräte & Dienste"
3. Klick: "+ Neue Integration erstellen"
4. Suche: "HACS"
5. Installiere HACS
6. Starte Home Assistant neu
```

#### Schritt 2: PyScript via HACS installieren
```
1. Öffne: HACS (oben rechts in HA)
2. Wähle: "Automation" (linkes Menü)
3. Oben: "Erkunden & Herunterladen Repositories"
4. Suche: "pyscript"
5. Klick: "pyscript by CustomComponents"
6. Klick: "INSTALL"
7. Bestätige Installation
8. Starte Home Assistant neu
```

#### Schritt 3: Dependencies automatisch laden
PyScript lädt Dependencies automatisch, wenn:

```yaml
# configuration.yaml
pyscript:
  allow_all_imports: true      # ← WICHTIG! Erlaubt Imports
  file_reloader: true          # ← Optional: Auto-Reload
```

Mit `allow_all_imports: true`:
- ✅ requests (wird heruntergeladen)
- ✅ yaml (wird heruntergeladen)
- ✅ hmac, hashlib, json (bereits in Python)

#### Schritt 4: Manuell prüfen/installieren
Wenn Dependencies nicht automatisch laden:

**Via SSH/Terminal Add-on:**
```bash
# SSH Terminal öffnen
ssh root@192.168.1.100  # (deine HA IP)

# Dependencies installieren
pip install requests pyyaml

# Oder für Home Assistant OS:
docker exec homeassistant pip install requests pyyaml
```

**Terminal Add-on in Home Assistant:**
```
Einstellungen → Zusatzprogramme → "Terminal & SSH"
oder
Einstellungen → Zusatzprogramme → Alle Add-ons anzeigen → "+ Terminal & SSH"
```

Dann im Terminal:
```bash
pip install requests pyyaml
```

#### Schritt 5: Verifikation
Prüfe ob alles funktioniert:

```python
# In PyScript oder Developer Tools → Python Shell
import requests
import yaml
print("✓ Alle Dependencies geladen!")
```

Oder via Home Assistant Developer Tools:
```
Developer Tools → Services
Suche: "pyscript"
Sollte Services anzeigen wie: pyscript.tuya_update_all
```

---

### Option 2: REST API (Einfach - Externe Python App)

**WICHTIG:** Option 2 ist KEIN PyScript - es ist eine separate Python App, die parallel läuft!

#### Architektur:

```
┌─────────────────────────────────────────┐
│        HOME ASSISTANT                   │
│  (REST Commands aufrufen)               │
└─────────────┬───────────────────────────┘
              │
              │ HTTP Requests
              │ (Port 5000)
              ▼
┌─────────────────────────────────────────┐
│    TUYA CLIENT REST API SERVER          │
│    (Separate Python App)                │
│  src/tuya_homeassistant_api.py          │
│                                         │
│  Läuft auf: localhost:5000              │
│  Oder: 192.168.1.100:5000               │
└─────────────┬───────────────────────────┘
              │
              │ HTTPS
              ▼
┌─────────────────────────────────────────┐
│      TUYA CLOUD API                     │
│      (Externe Server)                   │
└─────────────────────────────────────────┘
```

#### Step 1: REST API starten (Separate Terminal/Prozess)

**Option A: Lokale Maschine / Windows / Mac**

```bash
# In Terminal/PowerShell (NEUER Terminal!)
# Gehe ins Projekt-Verzeichnis
cd C:\Users\Minex\Documents\tuya\ Client

# API starten
python3 src/tuya_homeassistant_api.py --port 5000

# Output:
# ╔════════════════════════════════════════════════════════════╗
# ║  🏠 Tuya Client - Home Assistant REST API                 ║
# ╠════════════════════════════════════════════════════════════╣
# ║  Starting on 0.0.0.0:5000
```

Die App läuft jetzt im Hintergrund!

---

**Option A+: Auf Raspberry Pi (mit Home Assistant OS) laden**

##### ⚡ SCHNELL: Mit curl + Automatisches Installations-Skript

Dies ist die **einfachste Methode**!

```bash
# Auf dem Raspi (via SSH)
ssh root@192.168.1.100

# Einfach kopieren & einfügen:
curl -fsSL https://raw.githubusercontent.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/main/install_rest_api.sh | bash

# Das Skript macht ALLES:
# ✓ Python & git überprüfen/installieren
# ✓ Projekt von GitHub klonen
# ✓ Dependencies installieren (pip install)
# ✓ config.yaml erstellen (Credentials eingeben)
# ✓ Systemd Service einrichten (optional)
# ✓ Autostart konfigurieren
# ✓ Verifizierung durchführen
```

**Das war's!** Die API läuft jetzt unter `http://192.168.1.100:5000` 🎉

---

##### Manuelle Installation (Für Fortgeschrittene)

Wenn du lieber Schritt für Schritt vorgehen möchtest:

##### 1️⃣ Projekt auf den Raspi kopieren

**Via SSH (von deinem Computer aus):**

```powershell
# PowerShell auf deinem Computer

# 1. Ins Projekt-Verzeichnis gehen
cd "C:\Users\Minex\Documents\tuya Client"

# 2. Projekt auf Raspi kopieren
scp -r . root@192.168.1.100:/root/tuya_client

# oder mit curl (direkt auf Raspi):
# ssh root@192.168.1.100
# curl -o tuya_client.tar.gz https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/archive/refs/heads/main.tar.gz
# tar -xzf tuya_client.tar.gz -C /root/
```

**Alternative: Via Home Assistant UI (Samba Share)**

```
1. Gehe zu: Home Assistant → Einstellungen → Zusatzprogramme
2. Suche: "Samba Share"
3. Installiere & öffne
4. Auf deinem Computer: Netzwerk → \\192.168.1.100
5. Geben Sie Benutzername/Passwort ein
6. Kopiere dein Projekt in: config/www/tuya_client
```

---

##### 2️⃣ Auf Raspi mit SSH verbinden

```bash
# Von deinem Computer (Windows PowerShell)
ssh root@192.168.1.100
# Passwort eingeben

# Du solltest jetzt auf dem Raspi sein:
# root@homeassistant:~# _
```

---

##### 3️⃣ Credentials aktualisieren

```bash
# Im SSH Terminal des Raspi

# Zum Projekt gehen
cd /root/tuya_client

# tuya_homeassistant_api.py öffnen und Credentials eintragen
nano src/tuya_homeassistant_api.py

# Oder mit vi:
vi src/tuya_homeassistant_api.py
```

Bearbeite diese Zeilen:

```python
# Line ~15
TUYA_ACCESS_ID = "deine_access_id"
TUYA_ACCESS_KEY = "deine_access_key"
TUYA_DEVICE_ID = "deine_device_id"
TUYA_REGION = "eu"  # oder "us", "cn"
```

Speichern:
- **nano:** `Ctrl+O`, Enter, `Ctrl+X`
- **vi:** `:wq`, Enter

---

##### 4️⃣ Dependencies installieren

```bash
# Im SSH Terminal auf dem Raspi

# WICHTIG: Nutze nur core requirements (KEIN PyQt6!)
pip install -q -r requirements.txt

# Oder einzeln (einfacher):
pip install flask flask-cors pyyaml requests

# Verifizieren:
python3 -c "import flask, yaml, requests; print('✓ OK')"
```

**Hinweis:** PyQt6 ist optional (nur für Desktop GUI auf Linux/Windows)
- Nicht installieren auf Raspberry Pi (lange Kompilierung)
- REST API braucht nur: `flask`, `flask-cors`, `pyyaml`, `requests`

---

##### 5️⃣ API starten (Methode 1: Schnell-Test)

```bash
# Im SSH Terminal

cd /root/tuya_client
python3 src/tuya_homeassistant_api.py --port 5000

# Sollte zeigen:
# 🏠 Tuya Client - Home Assistant REST API
# Starting on 0.0.0.0:5000
```

Test (neues SSH Terminal):
```bash
curl http://localhost:5000/health
# Response: {"status": "ok"}
```

---

##### 5️⃣ API starten (Methode 2: Hintergrund - Permanent)

**Mit `screen` (empfohlen - einfach):**

```bash
# Screen installieren (falls nicht vorhanden)
apt-get update && apt-get install screen -y

# Neue Session erstellen
screen -S tuya_api

# Im Screen-Terminal die API starten
cd /root/tuya_client
python3 src/tuya_homeassistant_api.py --port 5000

# Detach (läuft im Hintergrund): Ctrl+A dann D
# Reattach (wiederherstellen): screen -r tuya_api
# Killing: screen -X -S tuya_api quit
```

**Mit `nohup` (noch einfacher):**

```bash
cd /root/tuya_client
nohup python3 src/tuya_homeassistant_api.py --port 5000 > tuya_api.log 2>&1 &

# Logs anschauen:
tail -f tuya_api.log
```

**Mit Systemd Service (Autostart beim Reboot):**

```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/tuya-api.service

# Folgendes einfügen:
```

```ini
[Unit]
Description=Tuya Client REST API
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/tuya_client
ExecStart=/usr/bin/python3 /root/tuya_client/src/tuya_homeassistant_api.py --port 5000
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
# Service aktivieren & starten
sudo systemctl daemon-reload
sudo systemctl enable tuya-api
sudo systemctl start tuya-api

# Status prüfen:
sudo systemctl status tuya-api

# Logs anschauen:
sudo journalctl -u tuya-api -f
```

---

##### 6️⃣ Von Home Assistant aus aufrufen

Jetzt funktioniert Option 2 REST API perfekt!

In `configuration.yaml`:

```yaml
rest_command:
  tuya_get_properties:
    url: "http://192.168.1.100:5000/properties"
    method: get
```

Der Raspi läuft im Hintergrund! 🎉

**Option B: Home Assistant Container**

```bash
# SSH in Home Assistant
ssh root@192.168.1.100

# Dependencies installieren
pip install flask flask-cors pyyaml

# API starten (im Hintergrund)
nohup python3 src/tuya_homeassistant_api.py --port 5000 &

# Oder mit Screen/Tmux für einfaches Management
screen -S tuya_api
python3 src/tuya_homeassistant_api.py --port 5000
# Detach: Ctrl+A dann D
# Reattach: screen -r tuya_api
```

**Option C: Als Systemd Service (Autostart)**

Erstelle `/etc/systemd/system/tuya-api.service`:

```ini
[Unit]
Description=Tuya Client REST API
After=network.target

[Service]
Type=simple
User=homeassistant
WorkingDirectory=/path/to/tuya_client
ExecStart=/usr/bin/python3 src/tuya_homeassistant_api.py --port 5000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Dann:
```bash
systemctl enable tuya-api
systemctl start tuya-api
systemctl status tuya-api
```

#### Step 2: In Home Assistant konfigurieren

**Wichtig:** REST API wird NICHT über PyScript verwendet!

Stattdessen nutzt du `rest_command` direkt:

```yaml
# /config/configuration.yaml

rest_command:
  tuya_get_properties:
    url: "http://192.168.1.100:5000/properties"
    method: get
  
  tuya_get_boolcode:
    url: "http://192.168.1.100:5000/boolcode"
    method: get
  
  tuya_set_property:
    url: "http://192.168.1.100:5000/set"
    method: post
    payload: '{"property":"{{ property }}", "value":{{ value }}}'
    content_type: application/json
  
  tuya_set_boolcode:
    url: "http://192.168.1.100:5000/boolcode"
    method: post
    payload: '{"value":"{{ value }}"}'
    content_type: application/json
```

Restart Home Assistant!

#### Step 3: REST Commands in Automationen nutzen

**Beispiel 1: Properties abrufen**

```yaml
automation:
  - alias: "Tuya: Properties aktualisieren"
    trigger:
      platform: time_pattern
      minutes: 5
    action:
      - service: rest_command.tuya_get_properties
```

**Beispiel 2: Property setzen**

```yaml
automation:
  - alias: "Tuya: Power an"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      - service: rest_command.tuya_set_property
        data:
          property: "Power"
          value: true
```

**Beispiel 3: boolCode setzen**

```yaml
automation:
  - alias: "Tuya: boolCode setzen"
    trigger:
      platform: state
      entity_id: input_text.tuya_boolcode
    action:
      - service: rest_command.tuya_set_boolcode
        data:
          value: "{{ states('input_text.tuya_boolcode') }}"
```

#### Step 4: Template Sensoren (Optional)

Erstelle Sensoren aus REST API Responses:

```yaml
template:
  - trigger:
      platform: time_pattern
      minutes: 5
    sensor:
      - name: "Tuya Temperature"
        unique_id: tuya_temp_current
        state: >
          {% set temp = state_attr('sensor.tuya_properties', 'temp_current') %}
          {{ (temp / 10) if temp else 'unknown' }}
        unit_of_measurement: "°C"
      
      - name: "Tuya Humidity"
        unique_id: tuya_humidity
        state: >
          {{ state_attr('sensor.tuya_properties', 'humidity_current') }}
        unit_of_measurement: "%"
```

#### Step 5: Dashboard nutzen

```yaml
views:
  - title: Tuya (REST API)
    cards:
      - type: entities
        title: Status
        entities:
          - entity: sensor.tuya_temperature
            name: "Temperature"
          - entity: sensor.tuya_humidity
            name: "Humidity"
      
      - type: custom:button-card
        name: "Set Cooling"
        tap_action:
          action: call-service
          service: rest_command.tuya_set_boolcode
          data:
            value: "cooling"
```

---

## 🆚 Vergleich: PyScript vs REST API

| Aspekt | PyScript (Option 1) | REST API (Option 2) |
|--------|-------------------|-------------------|
| **Installation** | HACS + PyScript Add-on | Python Script + Flask |
| **Läuft wo** | In Home Assistant | Separate Python App |
| **Dependencies** | Auto-geladen | Manuell: `pip install` |
| **Services** | Native HA Services | REST Commands |
| **Best für** | Home Assistant Profis | Flexible Setups |
| **Komplexität** | Mittel | Einfach |
| **Performance** | Optimal | Gut |
| **Fehlersuche** | HA Logs | API + HA Logs |

**Empfehlung:**
- **PyScript:** Du magst Home Assistant UI & native Integration
- **REST API:** Du magst externe Apps & Flexibilität


---

## 📱 Dashboard Beispiel

```yaml
views:
  - title: Tuya
    cards:
      - type: entities
        title: Status
        entities:
          - entity: sensor.tuya_power
            name: "Power"
          - entity: sensor.tuya_temp_current
            name: "Temperatur"
      
      - type: entities
        title: Kontrolle
        entities:
          - entity: input_boolean.tuya_power
            name: "Einschalten"
          - entity: input_number.tuya_temp_set
            name: "Solltemperatur"
          - entity: input_select.tuya_mode
            name: "Modus"
```

---

## 🔄 Automatisierungen

### Beispiel 1: Morgens einschalten
```yaml
automation:
  - alias: "Tuya morgens an"
    trigger:
      platform: time
      at: "06:00:00"
    action:
      - service: pyscript.tuya_set_property
        data:
          property_code: "Power"
          value: true
```

### Beispiel 2: Temperatur überwachen
```yaml
automation:
  - alias: "Tuya zu warm"
    trigger:
      platform: numeric_state
      entity_id: sensor.tuya_temp_current
      above: 28
    action:
      - service: pyscript.tuya_set_property
        data:
          property_code: "mode"
          value: "cool"
      - service: notify.mobile_app_handy
        data:
          message: "Zu warm! Kühlung aktiviert."
```

---

## 🎛️ Alle 35 Eigenschaften in HA

| Code | Typ | HA-Entity | Kontrolle |
|------|-----|-----------|-----------|
| `Power` | bool | `input_boolean.tuya_power` | Toggle |
| `temp_set` | number | `input_number.tuya_temp_set` | Slider |
| `temp_current` | number | `sensor.tuya_temp_current` | Display |
| `humidity_current` | number | `sensor.tuya_humidity_current` | Display |
| `mode` | select | `input_select.tuya_mode` | Dropdown |
| `windspeed` | select | `input_select.tuya_windspeed` | Dropdown |
| `airquality` | number | `sensor.tuya_airquality` | Display |
| `pm25` | number | `sensor.tuya_pm25` | Display |
| `energy` | select | `input_select.tuya_energy` | Dropdown |
| `sleep` | select | `input_select.tuya_sleep` | Dropdown |
| `dirty_filter` | bool | `input_boolean.tuya_dirty_filter` | Display |

*... + 24 weitere Sensoren*

---

## 🐛 Fehlersuche

**Problem: Services nicht vorhanden**
```
→ Home Assistant neu starten
→ PyScript im HACS neu laden
→ Logs checken: Einstellungen → System → Logs
```

**Problem: Keine Verbindung**
```
→ Credentials überprüfen
→ Tuya API erreichbar? (openapi.tuyaeu.com)
→ Netzwerkverbindung prüfen
```

**Problem: Werte aktualisieren nicht**
```
→ Update-Interval anpassen (default 5 min)
→ Manually trigger: Developer Tools → Services → tuya_update_all
```

---

## 📚 Weitere Ressourcen

- **Vollständige Docs**: `docs/HOMEASSISTANT_COMPLETE.md`
- **Praktische Beispiele**: `docs/HOMEASSISTANT_EXAMPLES.md`
- **Home Assistant**: https://www.home-assistant.io/
- **PyScript**: https://hacs-pyscript.readthedocs.io/

---

## ✅ Checkliste

- [ ] PyScript installiert (oder REST API laufen)
- [ ] Credentials eingetragen
- [ ] Home Assistant neu gestartet
- [ ] Services in Developer Tools sichtbar
- [ ] Dashboard erstellt
- [ ] Erste Automation getestet
- [ ] Benachrichtigungen konfiguriert

**Fertig! 🎉**
