# Home Assistant Integration - Visuelle Übersicht

## 🎯 Gesamtarchitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOME ASSISTANT                               │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         LOVELACE UI DASHBOARD                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Status   │  │ Controls │  │Properties│            │   │
│  │  └──────────┘  └──────────┘  └──────────┘            │   │
│  └────────────────────────────────────────────────────────┘   │
│                           ▲                                     │
│                           │                                     │
│                      (Automationen)                            │
│                           │                                     │
│  ┌────────────────────────────────────────────────────────┐   │
│  │   INTEGRATION LAYER (PyScript / REST)                  │   │
│  │                                                        │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │ PyScript Services / REST API Endpoints           │ │   │
│  │  │ - tuya_update_all()                              │ │   │
│  │  │ - tuya_set_property(code, value)                 │ │   │
│  │  │ GET/POST /properties, /set, /device              │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  └────────────────────────────────────────────────────────┘   │
│                           ▲                                     │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                   (HTTP / REST / Direct)
                            │
    ┌───────────────────────┴──────────────────────┐
    │                                               │
    ▼                                               ▼
┌──────────────────────────┐          ┌──────────────────────────┐
│   TUYA CLIENT            │          │  TUYA CLOUD API          │
│                          │          │  (Tuya Servers)          │
│ ┌────────────────────┐   │          │                          │
│ │ TuyaCloudClient    │   │          │ - Device Status          │
│ │                    │   │          │ - Property Values        │
│ │ get_token()        │───┼──────────▶ - Set Commands          │
│ │ get_properties()   │   │  HTTPS   │ - All 35+ Properties     │
│ │ set_property()     │───┼──────────▶                          │
│ │                    │   │          │ Region: EU/US/CN/etc     │
│ └────────────────────┘   │          │                          │
│                          │          └──────────────────────────┘
│ ┌────────────────────┐   │
│ │ Credentials        │   │
│ │ - access_id        │   │
│ │ - access_key       │   │
│ │ - device_id        │   │
│ └────────────────────┘   │
│                          │
│ src/tuya_homeassistant_  │
│ api.py (Optional)        │
│ ┌────────────────────┐   │
│ │ Flask REST API     │   │
│ │ Port 5000          │   │
│ └────────────────────┘   │
└──────────────────────────┘
```

---

## 📊 Entity Mapping (Alle 35+ Eigenschaften)

```
TUYA DEVICE PROPERTIES          HOME ASSISTANT ENTITIES         DASHBOARD CONTROL
═══════════════════════════════════════════════════════════════════════════════════

POWER & MAIN
└─ Power                ─────▶ input_boolean.tuya_power        ▶ [ON/OFF Toggle]
└─ dirty_filter        ─────▶ input_boolean.tuya_dirty_filter  ▶ [Alert Display]

TEMPERATURE
├─ temp_set            ─────▶ input_number.tuya_temp_set       ▶ [Slider 16-30°C]
├─ temp_current        ─────▶ sensor.tuya_temp_current         ▶ [Display + History]
└─ savemoney_temp      ─────▶ input_number.tuya_savemoney_temp ▶ [Eco Slider]

HUMIDITY & AIR QUALITY
├─ humidity_current    ─────▶ sensor.tuya_humidity_current     ▶ [Display + Graph]
├─ airquality          ─────▶ sensor.tuya_airquality           ▶ [Gauge: Poor/Good]
└─ pm25                ─────▶ sensor.tuya_pm25                 ▶ [Alert on High]

MODES & CONTROLS
├─ mode                ─────▶ input_select.tuya_mode           ▶ [Dropdown: Cool/Heat/Auto]
├─ windspeed           ─────▶ input_select.tuya_windspeed      ▶ [Dropdown: Low/Mid/High]
├─ sleep               ─────▶ input_select.tuya_sleep          ▶ [Dropdown: Off/1/2/3]
├─ style               ─────▶ input_select.tuya_style          ▶ [Dropdown: Manual/Smart]
└─ energy              ─────▶ input_select.tuya_energy         ▶ [Dropdown: On/Off]

FILTERS & STATUS
├─ freshair_filter     ─────▶ input_boolean.tuya_freshair_filter ▶ [Toggle]
├─ hot_cold_wind       ─────▶ input_boolean.tuya_hot_cold_wind  ▶ [Toggle]
└─ work_time           ─────▶ sensor.tuya_work_time            ▶ [Display]

SENSORS (READ-ONLY)
├─ boolCode            ─────▶ sensor.tuya_boolCode             ▶ [Display]
├─ SN_SW_ver           ─────▶ sensor.tuya_SN_SW_ver            ▶ [Display]
└─ [+18 weitere]       ─────▶ sensor.tuya_*                    ▶ [Display]
```

---

## 🔄 Workflow-Beispiele

### Szenario 1: Benutzer ändert Temperatur in Dashboard

```
User klickt Slider in HA
    ▼
input_number.tuya_temp_set aktualisiert
    ▼
Automation wird ausgelöst: state_changed
    ▼
Action: pyscript.tuya_set_property(property_code="temp_set", value=220)
    ▼
PyScript ruft client.set_device_property("temp_set", 220)
    ▼
HTTPS POST an Tuya Cloud API
    ▼
Tuya sendet Befehl an echtes Gerät
    ▼
Gerät führt Befehl aus
    ▼
Nächste Auto-Update liest neuen Wert
    ▼
Dashboard wird aktualisiert ✓
```

### Szenario 2: Gerät-Wert ändert sich (Sensor)

```
Echtes Tuya-Gerät misst neue Temperatur
    ▼
Auto-Update lädt alle Properties (alle 5 Min)
    ▼
PyScript / REST API abrufen: client.get_device_properties()
    ▼
HTTPS GET von Tuya Cloud API
    ▼
Ergebnis: {"temp_current": 255, "humidity_current": 60, ...}
    ▼
sensor.tuya_temp_current aktualisiert zu 255 (=25.5°C)
    ▼
Automation prüft Bedingungen
    ▼
Falls temp_current > 28: Automation "Too Hot" ausgelöst
    ▼
Action: Notification "Temperatur: 28°C" an Handy
    ▼
Optional: Automatisches Kühlen aktivieren
```

### Szenario 3: Komplexe Automation

```
trigger: time = 22:00 (Abends)
    ▼
condition: input_boolean.tuya_power == "on"
    ▼
action 1: pyscript.tuya_set_property("sleep", "sleep1")
action 2: pyscript.tuya_set_property("windspeed", "low")
action 3: pyscript.tuya_set_property("temp_set", 200)  # 20°C
    ▼
notify.mobile_app: "Schlafmodus aktiviert"
    ▼
Call script.tuya_set_eco_mode (Optional)
```

---

## 🎮 Dashboard Layout-Beispiele

### Option A: Einfach & Kompakt

```
┌─────────────────────────────────────┐
│      TUYA CONTROL - SIMPLE          │
├─────────────────────────────────────┤
│                                     │
│  🔴 POWER                           │
│  [       ON/OFF Toggle       ]      │
│                                     │
│  🌡️  TEMPERATURE                   │
│  [=========●=======]  22°C          │
│                                     │
│  💨 MODE                            │
│  [  Auto ▼  ]                       │
│                                     │
│  📊 STATUS                          │
│  Humidity:   60%                    │
│  PM2.5:      45 µg/m³              │
│  Air Quality: GOOD                  │
│                                     │
└─────────────────────────────────────┘
```

### Option B: Professionell & Informativ

```
┌──────────────────────────────────────────────────────┐
│    TUYA DEVICE - PROFESSIONAL DASHBOARD              │
├──────────────────────┬───────────────────────────────┤
│  STATUS              │  CONTROLS                     │
├──────────────────────┼───────────────────────────────┤
│                      │                               │
│ 🟢 Online            │ 🔴 POWER                     │
│ 📍 IP: 192.168.1.100 │ [ON] [OFF]                   │
│                      │                               │
│ Current: 25.5°C      │ Set Temperature: 22°C         │
│ Target:  22.0°C      │ [──────●────────] 16° ‖ 30°  │
│                      │                               │
│ Humidity: 62%        │ Betriebsart:                  │
│ PM2.5: 35 µg/m³      │ [Heat ▼] [Cool ▼] [Auto ▼]  │
│ Air Quality: GOOD ✓  │                               │
│                      │ Lüfter:                       │
│ Filter: OK ✓         │ [Low] [Mid] [High] [Auto]    │
│ FreshAir: OK ✓       │                               │
│                      │ Schlaf:                       │
│                      │ [OFF] [Sleep1] [Sleep2]      │
│                      │                               │
└──────────────────────┴───────────────────────────────┘
│  HISTORY & ALERTS                                    │
├────────────────────────────────────────────────────┤
│ [Temperatur-Graph letzte 24h]                      │
│ [Luftqualitäts-Warnung: PM2.5 > 100]              │
└────────────────────────────────────────────────────┘
```

---

## ⚙️ Konfigurationsfluss

```
SCHRITT 1: CREDENTIALS SAMMELN
┌─────────────────────────────┐
│ Tuya Developer Platform     │
│ - API Key (Access ID)       │
│ - API Secret (Access Key)   │
│ - Device UUID (Device ID)   │
│ - Region (EU/US/CN)         │
└──────────────────┬──────────┘
                  ▼
SCHRITT 2: TUYA CLIENT KONFIGURIEREN
┌─────────────────────────────┐
│ config.yaml                 │
│ access_id: xxx              │
│ access_key: yyy             │
│ device_id: zzz              │
│ region: eu                  │
└──────────────────┬──────────┘
                  ▼
SCHRITT 3: PYSCRIPT / REST API STARTEN
┌─────────────────────────────┐
│ Option A: PyScript          │
│ /config/pyscript/           │
│ tuya_client.py kopieren     │
│                             │
│ Option B: REST API          │
│ python3 tuya_homeassistant_ │
│ api.py --port 5000          │
└──────────────────┬──────────┘
                  ▼
SCHRITT 4: ENTITY HELPER ERSTELLEN
┌─────────────────────────────┐
│ Home Assistant              │
│ - input_boolean             │
│ - input_number              │
│ - input_select              │
│ - automation                │
└──────────────────┬──────────┘
                  ▼
SCHRITT 5: DASHBOARD BAUEN
┌─────────────────────────────┐
│ Lovelace UI                 │
│ - Entities hinzufügen       │
│ - Cards konfigurieren       │
│ - Automationen verbinden    │
└──────────────────┬──────────┘
                  ▼
FERTIG! ✓ Vollständige HA Integration
```

---

## 📈 Datenfluss - API Calls

### GET /properties

```
Home Assistant
        │
        ▼ GET /properties
┌─────────────────────────────────────────┐
│ Tuya Client Flask API                   │
│ ┌─────────────────────────────────────┐ │
│ │ 1. Get Token                        │ │
│ │    POST /v1.0/token?grant_type=1   │ │
│ │    Headers: client_id, sign, t      │ │
│ │    ▼                                 │ │
│ │    Token: "eyJ0eXAi..."             │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ 2. Get Properties                   │ │
│ │    GET /v1.0/iot-03/devices/{id}/   │ │
│ │    status                           │ │
│ │    Headers: client_id, token, sign  │ │
│ │    ▼                                 │ │
│ │    Properties: {                    │ │
│ │      "Power": true,                 │ │
│ │      "temp_current": 255,           │ │
│ │      ...                            │ │
│ │    }                                │ │
│ └─────────────────────────────────────┘ │
└────────────────────┬────────────────────┘
                     ▼ JSON Response
        Home Assistant
        sensor.tuya_* updated ✓
```

### POST /set (Benutzer setzt Wert)

```
User: Klick auf Dashboard-Button "Heizen"
        ▼
Automation ausgelöst
        ▼
Action: POST /set {"property": "mode", "value": "hot"}
        ▼
┌──────────────────────────────────────────┐
│ Tuya Client Flask API                    │
│ ┌──────────────────────────────────────┐ │
│ │ 1. Generate HMAC-SHA256 Signature    │ │
│ │    timestamp: 1702123456789          │ │
│ │    Payload: {commands: [{code, val}]}│ │
│ │    ▼                                  │ │
│ │    sign = HMAC-SHA256(...)           │ │
│ └──────────────────────────────────────┘ │
│ ┌──────────────────────────────────────┐ │
│ │ 2. POST Command to Tuya              │ │
│ │    POST /v1.0/iot-03/devices/{id}/   │ │
│ │    commands                          │ │
│ │    Headers: client_id, token, sign   │ │
│ │    Body: {commands: [{code, value}]} │ │
│ │    ▼                                  │ │
│ │    Response: {"success": true}       │ │
│ └──────────────────────────────────────┘ │
└────────────────────┬─────────────────────┘
                     ▼
     ✓ Command an Gerät gesendet
        │
        ▼ (Gerät führt aus)
   Benutzer sieht Änderung
   im nächsten Update
```

---

## 🔒 Sicherheit

```
┌─────────────────────────────────────────┐
│  SICHERHEIT - Multi-Layer               │
├─────────────────────────────────────────┤
│                                         │
│  Layer 1: Credentials Management        │
│  ├─ .gitignore: config.yaml             │
│  └─ config/ nur .example Files          │
│                                         │
│  Layer 2: API Authentication            │
│  ├─ HMAC-SHA256 Signature (alle Requests)
│  ├─ Timestamp + Nonce (Replay-Protection)
│  └─ access_id + access_key (Tuya API)  │
│                                         │
│  Layer 3: Transport Security            │
│  ├─ HTTPS only (zu Tuya)                │
│  └─ Optional: Auth-Header für REST API  │
│                                         │
│  Layer 4: Home Assistant                │
│  ├─ Firewall (Port 5000 nur lokal)      │
│  └─ SSL für HA Web UI                   │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📝 Zusammenfassung: Von 0 bis Kontrolle

| Schritt | Aktion | Zeit | Status |
|---------|--------|------|--------|
| 1 | Credentials bei Tuya sammeln | 10 min | ✅ |
| 2 | config.yaml erstellen | 5 min | ✅ |
| 3 | PyScript/REST API starten | 5 min | ✅ |
| 4 | HA Automationen konfigurieren | 15 min | ✅ |
| 5 | Dashboard bauen | 20 min | ✅ |
| **TOTAL** | | **55 Min** | **✅ LIVE** |

---

## 🚀 Schnelle Kommandos

```bash
# REST API starten
python3 src/tuya_homeassistant_api.py --port 5000

# CLI Test
curl http://localhost:5000/properties

# Set via REST
curl -X POST http://localhost:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"Power","value":true}'
```

**Fertig! Dein Tuya-Gerät ist jetzt in Home Assistant kontrollierbar.** 🎉
