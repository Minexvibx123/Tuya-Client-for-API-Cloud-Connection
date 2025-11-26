# 📝 REST API Payload Formate

## Schnell-Referenz für alle Endpoints

### 🔧 SET Endpoints - Die unterschiedlichen Formate

#### 1. Standard Properties (Numbers, Booleans)

**Format:**
```json
{
  "property": "PropertyName",
  "value": value_here
}
```

**Beispiele:**

```bash
# Boolean (Power)
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"Power", "value":true}'

# Number (Temperatur)
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"temp_set", "value":250}'

# String/Enum (Mode)
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"mode", "value":"cool"}'
```

**In Home Assistant (rest_command):**

```yaml
rest_command:
  tuya_set_property:
    url: "http://192.168.1.100:5000/set"
    method: post
    payload: '{"property":"{{ property }}", "value":{{ value }}}'
    content_type: application/json
```

**In Automation:**

```yaml
automation:
  - alias: "Set Power"
    action:
      - service: rest_command.tuya_set_property
        data:
          property: "Power"
          value: true

  - alias: "Set Temperature"
    action:
      - service: rest_command.tuya_set_property
        data:
          property: "temp_set"
          value: 250

  - alias: "Set Mode"
    action:
      - service: rest_command.tuya_set_property
        data:
          property: "mode"
          value: "cool"
```

---

#### 2. boolCode Property (STRING ONLY!)

**⚠️ WICHTIG:** boolCode ist ein **STRING**, nicht Boolean!

**Format:**
```json
{
  "value": "string_value_here"
}
```

**Beispiele:**

```bash
# boolCode via /boolcode Endpoint
curl -X POST http://192.168.1.100:5000/boolcode \
  -H "Content-Type: application/json" \
  -d '{"value":"cooling"}'

# Alternative: via /set Endpoint
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"boolCode", "value":"heating"}'
```

**In Home Assistant (rest_command):**

```yaml
rest_command:
  tuya_set_boolcode:
    url: "http://192.168.1.100:5000/boolcode"
    method: post
    payload: '{"value":"{{ boolcode_value }}"}'
    content_type: application/json
```

**In Automation:**

```yaml
automation:
  - alias: "Set boolCode to Cooling"
    action:
      - service: rest_command.tuya_set_boolcode
        data:
          boolcode_value: "cooling"

  - alias: "Set boolCode from Input Select"
    action:
      - service: rest_command.tuya_set_boolcode
        data:
          boolcode_value: "{{ states('input_select.tuya_boolcode_mode') }}"
```

**Verfügbare boolCode Werte:**
```
- "cooling"
- "heating"
- "auto"
- "on"
- "off"
- "standby"
- (und custom Werte die dein Gerät unterstützt)
```

---

#### 3. Batch - Mehrere Properties auf einmal

**Format:**
```json
{
  "properties": [
    {"property": "PropertyName1", "value": value1},
    {"property": "PropertyName2", "value": value2},
    ...
  ]
}
```

**Beispiel:**

```bash
curl -X POST http://192.168.1.100:5000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "properties": [
      {"property": "Power", "value": true},
      {"property": "temp_set", "value": 250},
      {"property": "mode", "value": "cool"}
    ]
  }'
```

**In Home Assistant:**

```yaml
automation:
  - alias: "Set Multiple Tuya Properties"
    action:
      - service: rest_command.tuya_batch_set
        data:
          properties:
            - property: "Power"
              value: true
            - property: "temp_set"
              value: 250
            - property: "mode"
              value: "cool"
```

---

## 🔍 GET Endpoints - Responses

### GET /properties
```bash
curl http://192.168.1.100:5000/properties
```

**Response:**
```json
{
  "success": true,
  "data": {
    "Power": true,
    "temp_set": 250,
    "temp_current": 230,
    "mode": "cool",
    "boolCode": "cooling",
    ...
  }
}
```

### GET /property/PropertyName
```bash
curl http://192.168.1.100:5000/property/Power
```

**Response:**
```json
{
  "success": true,
  "property": "Power",
  "value": true
}
```

### GET /boolcode
```bash
curl http://192.168.1.100:5000/boolcode
```

**Response:**
```json
{
  "success": true,
  "property": "boolCode",
  "value": "cooling",
  "type": "string",
  "description": "Device status code (string)"
}
```

### GET /health
```bash
curl http://192.168.1.100:5000/health
```

**Response (Erfolgreich):**
```json
{
  "status": "healthy",
  "connected": true,
  "properties_count": 35
}
```

**Response (Fehler):**
```json
{
  "status": "error",
  "connected": false,
  "error": "Failed to get access token"
}
```

---

## 📊 Value Typen Referenz

| Property | Typ | Beispiel | Bereich |
|----------|-----|---------|---------|
| Power | Boolean | `true` / `false` | - |
| temp_set | Number | `250` | 160-300 (×10°C) |
| temp_current | Number | `230` | - |
| mode | String/Enum | `"cool"` | cool, heat, auto, wind, dry |
| windspeed | String/Enum | `"high"` | low, mid, high, auto |
| boolCode | String | `"cooling"` | beliebig (device-spezifisch) |
| sleep | String/Enum | `"sleep1"` | off, sleep1, sleep2, sleep3 |
| dirty_filter | Boolean | `true` / `false` | - |
| energy | String/Enum | `"on"` | on, off |

---

## ⚠️ Häufige Fehler

**Fehler 1: boolCode als Boolean**
```json
// ❌ FALSCH
{"value": true}

// ✅ RICHTIG
{"value": "on"}
```

**Fehler 2: Number als String in Payload**
```json
// ❌ FALSCH (wenn es ein Number sein soll)
{"property": "temp_set", "value": "250"}

// ✅ RICHTIG
{"property": "temp_set", "value": 250}
```

**Fehler 3: Falsche REST Command Payload Syntax**
```yaml
# ❌ FALSCH (zu viele Anführungszeichen)
payload: '{"property":"{{ property }}", "value":"{{ value }}"}'

# ✅ RICHTIG (nur Value muss als String sein, wenn es String sein soll)
payload: '{"property":"{{ property }}", "value":{{ value }}}'
```

---

## 🧪 Test-Befehle

```bash
# Health Check
curl http://192.168.1.100:5000/health | jq

# Alle Properties auflisten
curl http://192.168.1.100:5000/properties | jq

# Spezifische Property
curl http://192.168.1.100:5000/property/Power | jq

# boolCode abrufen
curl http://192.168.1.100:5000/boolcode | jq

# Power einschalten
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"Power", "value":true}' | jq

# Temperatur auf 24°C setzen (= 240)
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"temp_set", "value":240}' | jq

# Mode auf Cool setzen
curl -X POST http://192.168.1.100:5000/set \
  -H "Content-Type: application/json" \
  -d '{"property":"mode", "value":"cool"}' | jq

# boolCode auf Cooling setzen
curl -X POST http://192.168.1.100:5000/boolcode \
  -H "Content-Type: application/json" \
  -d '{"value":"cooling"}' | jq
```

---

## 📖 Zusammenfassung

| Endpoint | Method | Payload Format | Beispiel |
|----------|--------|-----------------|----------|
| `/set` | POST | `{"property":"name", "value":value}` | `{"property":"Power", "value":true}` |
| `/boolcode` | POST | `{"value":"string"}` | `{"value":"cooling"}` |
| `/batch` | POST | `{"properties":[{...}]}` | `{"properties":[{"property":"Power","value":true}]}` |
| `/properties` | GET | - | - |
| `/property/<name>` | GET | - | - |
| `/boolcode` | GET | - | - |
| `/health` | GET | - | - |

