# Home Assistant Integration - Schnellstart

## 🚀 5-Minuten Setup

### Option 1: PyScript (Empfohlen - Vollständig)

**1. PyScript installieren**
```
Home Assistant → Einstellungen → Zusatzprogramme → PyScript
```

**2. Datei erstellen**
```
/config/pyscript/tuya_client.py
```
Kopiere Inhalt aus `docs/HOMEASSISTANT_COMPLETE.md` (tuya_client.py Sektion)

**3. Credentials eintragen**
```python
TUYA_ACCESS_ID = "xxxxx"
TUYA_ACCESS_KEY = "xxxxx"
TUYA_DEVICE_ID = "xxxxx"
```

**4. Home Assistant neu starten**

**5. Lovelace Dashboard nutzen**
```yaml
- entity: input_boolean.tuya_power
  name: "Power"
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
