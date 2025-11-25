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

### Option 2: REST API (Einfach)

**1. Python-Dependencies installieren**
```bash
pip install flask flask-cors pyyaml
```

**2. API starten**
```bash
python3 src/tuya_homeassistant_api.py --port 5000
```

**3. In Home Assistant konfigurieren**
```yaml
# configuration.yaml
rest_command:
  tuya_get_properties:
    url: "http://192.168.1.100:5000/properties"
    method: get
  
  tuya_set_property:
    url: "http://192.168.1.100:5000/set"
    method: post
    payload: '{"property":"{{ property }}", "value":{{ value }}}'

template:
  - sensor:
      - name: "Tuya Temperature"
        unique_id: tuya_temp
        state: "{{ (states('input_number.tuya_temp_current') | float(0)) / 10 }}"
```

**4. Services erstellen**
```yaml
automation:
  - alias: "Tuya Control"
    trigger: ...
    action:
      - service: rest_command.tuya_set_property
        data:
          property: "Power"
          value: 1
```

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
