# Home Assistant Integration - Complete Guide

## Overview

Integrate Tuya Client with Home Assistant to:
- ✅ View all 35+ device properties as entities
- ✅ Create interactive dashboards
- ✅ Set values via Home Assistant UI
- ✅ Automate with Home Assistant automations
- ✅ Use in Node-RED, custom automations, etc.

## Installation Methods

### Method 1: PyScript (Recommended - Most Flexible)

#### Prerequisites
1. Home Assistant running (minimum 2021.12.0)
2. HACS installed
3. PyScript addon installed
4. Dependencies: `requests`, `yaml`, `hmac`, `hashlib`, `json` (mostly built-in)

#### Step 0: Understanding Dependencies

PyScript needs these Python packages:
- **requests** - HTTP calls to Tuya API
- **pyyaml** - Read YAML configs
- **Standard libs** - hmac, hashlib, json, time, logging (included with Python)

These are installed automatically if you set `allow_all_imports: true`

For manual installation, see: `docs/PYSCRIPT_DEPENDENCIES.md`

#### Step 1: Install PyScript via HACS

```
1. Home Assistant → Settings → Devices & Services
2. Click "+ Create Automation"
3. Search: "HACS"
4. Install HACS first (if not installed)
5. Then: HACS → Automation → Search "PyScript"
6. Click "pyscript"
7. Click "INSTALL"
8. Restart Home Assistant
```

Detailed guide: `docs/PYSCRIPT_DEPENDENCIES.md`

#### Step 2: Enable PyScript in configuration.yaml

```yaml
pyscript:
  allow_all_imports: true    # ← IMPORTANT! Auto-loads dependencies
  file_reloader: true
```

**IMPORTANT:** Without `allow_all_imports: true`, dependencies won't be imported!

Restart Home Assistant:
```
Settings → System → "Restart Home Assistant"
```

Verify success:
```
Developer Tools → Services
Search: "pyscript"
Should show: pyscript.tuya_update_all, etc.
```

#### Step 3: Create Tuya Client PyScript

Create file: `/config/pyscript/tuya_client.py`

```python
"""
Tuya Client for Home Assistant
Reads and writes all device properties as entities
"""

import logging
import json
from typing import Any, Dict
import requests
import hmac
import hashlib
import time

_LOGGER = logging.getLogger(__name__)

# Configuration - UPDATE THESE
TUYA_ACCESS_ID = "your_access_id"
TUYA_ACCESS_KEY = "your_access_key"
TUYA_DEVICE_ID = "your_device_id"
TUYA_REGION = "eu"

# API Endpoint
BASE_URL = f"https://openapi.tuya{TUYA_REGION}.com"

class TuyaClient:
    """Tuya Cloud API Client"""
    
    def __init__(self):
        self.access_id = TUYA_ACCESS_ID
        self.access_key = TUYA_ACCESS_KEY
        self.device_id = TUYA_DEVICE_ID
        self.base_url = BASE_URL
        self.token = None
    
    def _get_signature(self, method, path, content=""):
        """Calculate HMAC-SHA256 signature"""
        timestamp = str(int(time.time() * 1000))
        content_hash = hashlib.sha256(content.encode() if content else b"").hexdigest()
        
        string_to_sign = f"{method}\n{content_hash}\n\n{path}"
        sign = hmac.new(
            self.access_key.encode(),
            (self.access_id + self.token + timestamp + string_to_sign).encode(),
            hashlib.sha256
        ).hexdigest().upper()
        
        return sign, timestamp
    
    def get_token(self) -> bool:
        """Get access token"""
        method = "GET"
        path = "/v1.0/token?grant_type=1"
        
        timestamp = str(int(time.time() * 1000))
        content_hash = hashlib.sha256(b"").hexdigest()
        
        string_to_sign = f"{method}\n{content_hash}\n\n{path}"
        sign = hmac.new(
            self.access_key.encode(),
            (self.access_id + timestamp + string_to_sign).encode(),
            hashlib.sha256
        ).hexdigest().upper()
        
        headers = {
            "client_id": self.access_id,
            "sign": sign,
            "t": timestamp,
            "sign_method": "HMAC-SHA256"
        }
        
        try:
            response = requests.get(f"{self.base_url}{path}", headers=headers, timeout=10)
            data = response.json()
            if data.get("success"):
                self.token = data["result"]["access_token"]
                _LOGGER.info("✓ Tuya token obtained")
                return True
        except Exception as e:
            _LOGGER.error(f"✗ Token error: {e}")
        
        return False
    
    def get_properties(self) -> Dict[str, Any]:
        """Get all device properties"""
        if not self.token:
            if not self.get_token():
                return {}
        
        method = "GET"
        path = f"/v1.0/iot-03/devices/{self.device_id}/status"
        
        sign, timestamp = self._get_signature(method, path)
        
        headers = {
            "client_id": self.access_id,
            "access_token": self.token,
            "sign": sign,
            "t": timestamp,
            "sign_method": "HMAC-SHA256"
        }
        
        try:
            response = requests.get(f"{self.base_url}{path}", headers=headers, timeout=10)
            data = response.json()
            if data.get("success"):
                return {item["code"]: item["value"] for item in data["result"]}
        except Exception as e:
            _LOGGER.error(f"✗ Properties error: {e}")
        
        return {}
    
    def set_property(self, code: str, value: Any) -> bool:
        """Set device property"""
        if not self.token:
            if not self.get_token():
                return False
        
        method = "POST"
        path = f"/v1.0/iot-03/devices/{self.device_id}/commands"
        
        payload = {
            "commands": [
                {"code": code, "value": value}
            ]
        }
        content = json.dumps(payload)
        
        sign, timestamp = self._get_signature(method, path, content)
        
        headers = {
            "client_id": self.access_id,
            "access_token": self.token,
            "sign": sign,
            "t": timestamp,
            "sign_method": "HMAC-SHA256",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}{path}",
                headers=headers,
                data=content,
                timeout=10
            )
            data = response.json()
            if data.get("success"):
                _LOGGER.info(f"✓ Set {code} = {value}")
                return True
            else:
                _LOGGER.error(f"✗ Set failed: {data}")
        except Exception as e:
            _LOGGER.error(f"✗ Set error: {e}")
        
        return False

# Global client
client = TuyaClient()

@service
def tuya_update_all():
    """Update all Tuya properties as sensors"""
    _LOGGER.info("Updating all Tuya properties...")
    
    props = client.get_properties()
    if not props:
        _LOGGER.error("Failed to get properties")
        return
    
    for code, value in props.items():
        # Create sensor state
        entity_id = f"sensor.tuya_{code}"
        hass.set_state(entity_id, value)
        
        _LOGGER.debug(f"{code}: {value}")

@service
def tuya_set_property(property_code: str, value: Any):
    """Set a Tuya property value"""
    _LOGGER.info(f"Setting {property_code} to {value}")
    
    if client.set_property(property_code, value):
        # Update state immediately
        entity_id = f"sensor.tuya_{property_code}"
        hass.set_state(entity_id, value)
        task.sleep(1)
        tuya_update_all()

@service
def tuya_get_boolcode():
    """Get boolCode property (DP_ID 123)"""
    _LOGGER.info("Getting boolCode...")
    
    props = client.get_properties()
    boolcode_value = props.get("boolCode")
    
    if boolcode_value is not None:
        _LOGGER.info(f"boolCode: {boolcode_value}")
        hass.set_state("sensor.tuya_boolcode", boolcode_value)
        return boolcode_value
    else:
        _LOGGER.error("boolCode not found")
        return None

@service
def tuya_set_boolcode(value: str):
    """Set boolCode property (DP_ID 123) - Custom status string"""
    _LOGGER.info(f"Setting boolCode to: {value}")
    
    if client.set_property("boolCode", str(value)):
        hass.set_state("sensor.tuya_boolcode", str(value))
        _LOGGER.info(f"✓ boolCode set to: {value}")
        task.sleep(1)
        tuya_update_all()
        return True
    else:
        _LOGGER.error(f"✗ Failed to set boolCode")
        return False

@service
def tuya_create_entities():
    """Create input helpers for all Tuya properties"""
    _LOGGER.info("Creating Tuya entities...")
    
    # Property type mapping
    bool_properties = ["Power", "dirty_filter", "freshair_filter", "hot_cold_wind"]
    enum_properties = ["mode", "windspeed", "sleep", "style", "energy"]
    value_properties = ["temp_set", "temp_current", "humidity_current", "pm25"]
    readonly_properties = ["temp_current", "humidity_current", "airquality", "pm25"]
    
    props = client.get_properties()
    
    for code, value in props.items():
        if code in readonly_properties:
            # Read-only: Create as sensor
            hass.call_service(
                "template_sensor",
                "reload"
            )
        elif code in bool_properties:
            # Boolean: Create input_boolean
            entity_id = f"input_boolean.tuya_{code}"
            hass.call_service(
                "input_boolean",
                "turn_on" if value else "turn_off",
                entity_id=entity_id
            )
        elif code in enum_properties:
            # Enum: Create input_select
            entity_id = f"input_select.tuya_{code}"
            hass.set_state(entity_id, str(value))
        elif code in value_properties:
            # Numeric: Create input_number
            entity_id = f"input_number.tuya_{code}"
            hass.set_state(entity_id, float(value) if isinstance(value, (int, float)) else 0)
    
    _LOGGER.info("✓ Entities created")

# Auto-update every 5 minutes
@task_unique("tuya_update")
async def auto_update():
    """Auto-update loop"""
    while True:
        tuya_update_all()
        await task.sleep(300)  # 5 minutes

# Start auto-update
task.create(auto_update())
```

#### Step 4: Create Lovelace Dashboard

Edit `ui-lovelace.yaml` or use UI editor:

```yaml
views:
  - title: Tuya Device
    cards:
      - type: vertical-stack
        cards:
          # Status Card
          - type: entities
            title: Device Status
            entities:
              - entity: sensor.tuya_temp_current
                name: Current Temperature
              - entity: sensor.tuya_humidity_current
                name: Humidity
              - entity: sensor.tuya_power
                name: Power Status
          
          # Control Card
          - type: entities
            title: Controls
            entities:
              - entity: input_boolean.tuya_power
                name: Power
              - entity: input_number.tuya_temp_set
                name: Set Temperature
              - entity: input_select.tuya_mode
                name: Mode
              - entity: input_select.tuya_windspeed
                name: Wind Speed
          
          # Properties Card
          - type: entities
            title: All Properties
            entities:
              - entity: sensor.tuya_airquality
              - entity: sensor.tuya_pm25
              - entity: sensor.tuya_energy
              - entity: input_number.tuya_savemoney_temp
              - entity: input_select.tuya_sleep
```

#### Step 5: Create Automations

**Example 1: Temperature Control Automation**

```yaml
automation:
  - alias: "Tuya: Auto Heat when Cold"
    trigger:
      platform: numeric_state
      entity_id: sensor.tuya_temp_current
      below: 18
    action:
      - service: pyscript.tuya_set_property
        data:
          property_code: "mode"
          value: "hot"
      - service: pyscript.tuya_set_property
        data:
          property_code: "temp_set"
          value: 220  # 22°C

  - alias: "Tuya: Power off at Night"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      - service: pyscript.tuya_set_property
        data:
          property_code: "Power"
          value: false
```

**Example 2: Sync with Input Boolean**

```yaml
automation:
  - alias: "Tuya: Sync Power Control"
    trigger:
      platform: state
      entity_id: input_boolean.tuya_power
    action:
      - service: pyscript.tuya_set_property
        data:
          property_code: "Power"
          value: "{{ trigger.to_state.state }}"
```

### Method 2: RESTful Integration (Alternative)

If PyScript is not available, use RESTful:

```yaml
rest_command:
  tuya_set_property:
    url: "http://tuya-client-host:5000/set"
    method: POST
    payload: '{"property":"{{ property }}", "value":{{ value }}}'
    headers:
      Content-Type: application/json

template:
  - sensor:
      - name: "Tuya Temperature"
        unique_id: tuya_temp
        unit_of_measurement: "°C"
        state: "{{ (states('input_number.tuya_temp_current') | float(0)) / 10 }}"
```

## Entity Mapping

| Property | Type | Entity | Control |
|----------|------|--------|---------|
| Power | bool | `input_boolean.tuya_power` | Toggle |
| temp_set | value | `input_number.tuya_temp_set` | Slider |
| temp_current | value | `sensor.tuya_temp_current` | Display |
| mode | enum | `input_select.tuya_mode` | Dropdown |
| windspeed | enum | `input_select.tuya_windspeed` | Dropdown |
| humidity_current | value | `sensor.tuya_humidity_current` | Display |
| airquality | value | `sensor.tuya_airquality` | Display |
| pm25 | value | `sensor.tuya_pm25` | Display |

## Lovelace UI Examples

### Thermostat Card

```yaml
type: thermostat
entity: climate.tuya_device
```

### Button Card

```yaml
type: button
name: "Heat Mode"
tap_action:
  action: call-service
  service: pyscript.tuya_set_property
  data:
    property_code: "mode"
    value: "hot"
```

### Gauge Card

```yaml
type: gauge
entity: sensor.tuya_temp_current
min: 10
max: 30
```

### History Stats Card

```yaml
type: history-stats
title: "Power Usage"
entity: input_boolean.tuya_power
state: "on"
period: day
```

## Troubleshooting

### Services Not Appearing
- Restart Home Assistant after PyScript install
- Check `/config/pyscript/` folder exists
- Verify `pyscript:` in `configuration.yaml`

### Entities Not Creating
- Check Home Assistant logs for errors
- Verify API credentials are correct
- Ensure device is online

### Values Not Updating
- Check PyScript logs
- Verify network connectivity
- Check API rate limits

### Wrong Property Values
- Verify property codes in PyScript
- Check value type (bool, int, string)
- Use developer tools to debug

## Performance Tuning

Adjust update frequency in PyScript:

```python
# Fast (every minute)
await task.sleep(60)

# Balanced (every 5 minutes) - DEFAULT
await task.sleep(300)

# Slow (every 10 minutes)
await task.sleep(600)
```

## Security Best Practices

1. **Never commit credentials** - Use secrets in PyScript:

```python
# Instead of hardcoding
TUYA_ACCESS_ID = "{{ secrets.tuya_access_id }}"
TUYA_ACCESS_KEY = "{{ secrets.tuya_access_key }}"
```

2. **Use HTTPS only** - Enable SSL in Home Assistant

3. **Firewall** - Restrict access to Home Assistant port

4. **Update regularly** - Keep Home Assistant and PyScript updated

## Advanced: Custom Services

Create custom services for complex operations:

```python
@service
def tuya_heating_mode(target_temp: float):
    """Set heating mode with target temperature"""
    client.set_property("mode", "hot")
    # Convert Celsius to Tuya format (×10)
    tuya_temp = int(target_temp * 10)
    client.set_property("temp_set", tuya_temp)

@service
def tuya_eco_mode():
    """Enable eco/save mode"""
    client.set_property("mode", "wind")
    client.set_property("windspeed", "auto")
    client.set_property("savemoney_temp", 160)  # 16°C
```

Use in automation:

```yaml
service: pyscript.tuya_heating_mode
data:
  target_temp: 22
```

## boolCode Property (DP_ID 123)

### Overview

`boolCode` is a string property (DP_ID 123) that allows setting and reading custom device status codes.

### PyScript Usage

**Get boolCode:**
```python
@service
def get_boolcode_value():
    """Get current boolCode value"""
    result = pyscript.tuya_get_boolcode()
    _LOGGER.info(f"boolCode: {result}")

# Call it:
# pyscript.get_boolcode_value()
```

**Set boolCode:**
```yaml
automation:
  - alias: "Set boolCode Status"
    trigger: ...
    action:
      - service: pyscript.tuya_set_boolcode
        data:
          value: "cooling"
```

### REST API Usage

**Get boolCode:**
```bash
curl http://localhost:5000/boolcode
# Returns:
# {"success": true, "property": "boolCode", "value": "cooling", "type": "string"}
```

**Set boolCode:**
```bash
curl -X POST http://localhost:5000/boolcode \
  -H "Content-Type: application/json" \
  -d '{"value":"heating"}'
# Returns:
# {"success": true, "property": "boolCode", "value": "heating"}
```

### Home Assistant Dashboard

**Create input_text helper for boolCode:**

```yaml
# configuration.yaml
input_text:
  tuya_boolcode:
    name: "Device Status Code"
    min: 0
    max: 100
```

**Dashboard card:**

```yaml
type: entities
entities:
  - entity: input_text.tuya_boolcode
    name: "Device Status"
  - entity: sensor.tuya_boolcode
    name: "Current Status (readonly)"
```

**Automation to sync:**

```yaml
automation:
  - alias: "Sync boolCode"
    trigger:
      platform: state
      entity_id: input_text.tuya_boolcode
    action:
      - service: pyscript.tuya_set_boolcode
        data:
          value: "{{ states('input_text.tuya_boolcode') }}"
```

### Common boolCode Values

| Value | Meaning |
|-------|---------|
| `on` | Device powered on |
| `off` | Device powered off |
| `cooling` | In cooling mode |
| `heating` | In heating mode |
| `idle` | Idle/standby |
| `error` | Error state |

*Note: Supported values depend on your specific Tuya device configuration.*

## Resources

- [Home Assistant Docs](https://www.home-assistant.io/)
- [PyScript Documentation](https://hacs-pyscript.readthedocs.io/)
- [Tuya API Reference](https://developer.tuya.com/)
- [Lovelace UI](https://www.home-assistant.io/lovelace/)

## Summary

✅ Full Home Assistant integration complete with:
- 35+ properties as entities
- Interactive controls
- Automations
- Custom dashboards
- Real-time updates
- **boolCode support (DP_ID 123)**

