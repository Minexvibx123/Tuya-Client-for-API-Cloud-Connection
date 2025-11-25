# boolCode Quick Reference 🚀

## Sofort verwenden

### REST API (cURL)

**Auslesen:**
```bash
curl http://localhost:5000/boolcode
```

**Setzen:**
```bash
curl -X POST http://localhost:5000/boolcode \
  -H "Content-Type: application/json" \
  -d '{"value":"cooling"}'
```

---

### Home Assistant Automation

**Setzen in Automation:**
```yaml
action:
  - service: pyscript.tuya_set_boolcode
    data:
      value: "heating"
```

**Auslesen in Automation:**
```yaml
action:
  - service: pyscript.tuya_get_boolcode
```

---

### Dashboard

**Entity:**
```yaml
entity: input_text.tuya_boolcode  # Zum Setzen
entity: sensor.tuya_boolcode      # Zum Auslesen
```

**Card:**
```yaml
type: entities
entities:
  - entity: sensor.tuya_boolcode
    name: "Status (Read-Only)"
  - entity: input_text.tuya_boolcode
    name: "Set Status"
```

---

## Eigenschaften

| Property | Value |
|----------|-------|
| **Code** | `boolCode` |
| **DP_ID** | `123` |
| **Type** | `string` |
| **Writable** | ✅ Ja |
| **Examples** | on, off, cooling, heating, idle |

---

## Was ist neu?

✅ `GET /boolcode` Endpoint  
✅ `POST /boolcode` Endpoint  
✅ `pyscript.tuya_get_boolcode()` Service  
✅ `pyscript.tuya_set_boolcode(value)` Service  
✅ Dashboard Helper: `input_text.tuya_boolcode`  

---

## Beispiele

### 1. Beim Starten Modus setzen
```yaml
automation:
  trigger:
    platform: homeassistant
    event: start
  action:
    - service: pyscript.tuya_set_boolcode
      data:
        value: "auto"
```

### 2. Bei Temperature-Schwellenwert
```yaml
automation:
  trigger:
    platform: numeric_state
    entity_id: sensor.tuya_temp_current
    above: 28
  action:
    - service: pyscript.tuya_set_boolcode
      data:
        value: "cooling"
```

### 3. Button im Dashboard
```yaml
type: custom:button-card
name: "Cool"
tap_action:
  action: call-service
  service: pyscript.tuya_set_boolcode
  data:
    value: "cooling"
```

---

## Docs

📖 **Vollständig:** `docs/HOMEASSISTANT_COMPLETE.md`  
📋 **Beispiele:** `docs/HOMEASSISTANT_EXAMPLES.md`  
🎨 **Architektur:** `docs/HOMEASSISTANT_ARCHITECTURE.md`  
📚 **Support:** `BOOLCODE_SUPPORT.md`  

---

**Viel Erfolg! 🎉**
