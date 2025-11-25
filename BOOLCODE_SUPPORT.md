# boolCode Support - Vollständige Implementierung ✅

## Was wurde hinzugefügt?

### 🔌 REST API Endpoints für boolCode

**GET /boolcode** - boolCode auslesen
```bash
curl http://localhost:5000/boolcode

Response:
{
  "success": true,
  "property": "boolCode",
  "value": "cooling",
  "type": "string",
  "description": "Device status code (string)"
}
```

**POST /boolcode** - boolCode setzen
```bash
curl -X POST http://localhost:5000/boolcode \
  -H "Content-Type: application/json" \
  -d '{"value":"heating"}'

Response:
{
  "success": true,
  "property": "boolCode",
  "value": "heating",
  "type": "string"
}
```

---

## 🏠 PyScript Services für Home Assistant

### tuya_get_boolcode()
```yaml
Aktion: pyscript.tuya_get_boolcode

Result: Liest aktuellen boolCode-Wert
        Speichert in: sensor.tuya_boolcode
        Gibt Wert zurück
```

### tuya_set_boolcode(value)
```yaml
Aktion: pyscript.tuya_set_boolcode
Data:
  value: "cooling"  # oder "heating", "idle", etc.

Result: Setzt boolCode auf Device
        Aktualisiert sensor.tuya_boolcode
        Aktualisiert alle Properties
```

---

## 📋 Home Assistant Konfiguration

### 1. Input Helper erstellen

```yaml
# configuration.yaml oder helpers.yaml
input_text:
  tuya_boolcode:
    name: "Device Status Code"
    icon: mdi:information
```

### 2. Automationen

**boolCode synchronisieren:**
```yaml
automation:
  - alias: "Sync boolCode"
    trigger:
      platform: state
      entity_id: input_text.tuya_boolcode
    action:
      - service: pyscript.tuya_set_boolcode
        data:
          value: "{{ trigger.to_state.state }}"
```

**boolCode periodisch auslesen:**
```yaml
automation:
  - alias: "Read boolCode"
    trigger:
      platform: time_pattern
      minutes: 5
    action:
      - service: pyscript.tuya_get_boolcode
```

### 3. Dashboard Card

```yaml
type: entities
title: "Device Status"
entities:
  - entity: sensor.tuya_boolcode
    name: "Current Status (Read-Only)"
  - entity: input_text.tuya_boolcode
    name: "Set Status"
```

### 4. Button Cards für Quick-Control

```yaml
type: custom:button-card
name: "🟢 Cooling"
tap_action:
  action: call-service
  service: pyscript.tuya_set_boolcode
  data:
    value: "cooling"
```

---

## 🔧 Technische Details

### Property Informationen

| Feld | Wert |
|------|------|
| **Property Code** | `boolCode` |
| **DP_ID** | `123` |
| **Type** | `string` |
| **Read-Write** | ✅ Beides möglich |
| **Description** | Device status code |

### Unterstützte Werte (Beispiele)

```
"on"       - Gerät an
"off"      - Gerät aus
"cooling"  - Im Kühl-Modus
"heating"  - Im Heiz-Modus
"idle"     - Ruhezustand
"error"    - Fehler-Status
"auto"     - Auto-Modus
```

*Hinweis: Tatsächlich unterstützte Werte hängen vom Tuya Gerät ab.*

---

## 📝 REST API Schemas

**GET /schemas** zeigt jetzt boolCode Details:

```json
{
  "string": {
    "boolCode": {
      "description": "Device status code (DP_ID 123)",
      "readonly": false,
      "examples": ["on", "off", "cooling", "heating", "auto"],
      "note": "Set custom string values to control or display device status"
    }
  }
}
```

---

## 🎯 Praktische Anwendungsfälle

### Szenario 1: Status Dashboard
```
Dashboard zeigt: sensor.tuya_boolcode
Benutzer klickt Button "Cooling"
  ↓
Automation setzt: input_text.tuya_boolcode = "cooling"
  ↓
Andere Automation triggert
  ↓
pyscript.tuya_set_boolcode("cooling")
  ↓
Device erhält Befehl
  ↓
Nächstes Update: sensor.tuya_boolcode = "cooling"
  ↓
Dashboard aktualisiert ✓
```

### Szenario 2: Komplexe Automation
```
Bedingung: temp_current > 28°C
  ↓
Action 1: pyscript.tuya_set_boolcode("cooling")
Action 2: pyscript.tuya_set_property("mode", "cool")
Action 3: Notification: "Auto-Cooling aktiviert"
  ↓
Result: Device kühlt automatisch
```

### Szenario 3: Fehler-Monitoring
```
Trigger: state = "error"
  ↓
Action 1: pyscript.tuya_get_boolcode()
Action 2: Benachrichtigung mit aktuellem Status
Action 3: Logger: "Device Error: {value}"
  ↓
Result: Admin benachrichtigt
```

---

## 🚀 Schnellstart

### 1. REST API testen
```bash
# Lesen
curl http://localhost:5000/boolcode

# Schreiben
curl -X POST http://localhost:5000/boolcode \
  -H "Content-Type: application/json" \
  -d '{"value":"heating"}'
```

### 2. In HA verwenden
```yaml
# Automation
action:
  - service: pyscript.tuya_set_boolcode
    data:
      value: "cooling"
```

### 3. Dashboard anpassen
```yaml
type: entities
entities:
  - entity: input_text.tuya_boolcode
    name: "Device Status"
```

---

## ✅ Features

✓ **GET boolCode** - Auslesen
✓ **SET boolCode** - Setzen (String-Werte)
✓ **PyScript Services** - Home Assistant Integration
✓ **REST Endpoints** - Flexible API
✓ **Dashboard Cards** - UI-Elemente
✓ **Automationen** - Komplexe Flows
✓ **Schema Info** - Type-Informationen
✓ **Error Handling** - Robuste Fehlerbehandlung

---

## 📚 Dokumentation

Vollständige Dokumentation in:
- `docs/HOMEASSISTANT_COMPLETE.md` - PyScript Code + Beispiele
- `docs/HOMEASSISTANT_EXAMPLES.md` - Automationen + Dashboard
- `docs/HOMEASSISTANT_ARCHITECTURE.md` - Entity Mapping

---

## 🔗 Alle Endpoints im Überblick

```
GET  /status              - Device Status
GET  /properties          - Alle Properties
GET  /property/<code>     - Single Property
POST /set                 - Property setzen
POST /batch               - Batch Setting
GET  /device              - Device Info
GET  /schemas             - Type Schemas
GET  /health              - Health Check
✨ GET  /boolcode          - Get boolCode
✨ POST /boolcode          - Set boolCode
GET  /api/v1/ha-entities - HA Entities
```

---

## 🎉 Zusammenfassung

**boolCode ist jetzt vollständig integriert:**

✅ REST API mit dedizierten Endpoints  
✅ PyScript Services für Home Assistant  
✅ Dashboard-kompatible Helpers  
✅ Umfassende Dokumentation  
✅ Production-ready Code  
✅ Error Handling & Validation  

**Du kannst jetzt boolCode-Werte setzen und auslesen!** 🚀
