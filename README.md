# Tuya Cloud Client - Enterprise Edition

Universal Python client library for controlling Tuya Smart Home devices via Tuya Cloud API. Provides complete device management, property control, and status monitoring capabilities.

## Overview

This project implements a comprehensive solution for interacting with Tuya Smart Home devices through the official Cloud API. It includes:

- Complete device status retrieval and monitoring
- Property reading and writing capabilities
- Modern graphical user interface for device control
- Command-line interface for automation and scripting
- Home Assistant integration via PyScript
- Type-aware property handling and validation

## Features

### Device Management
- Retrieve device status (online/offline, IP address, device information)
- List all available device properties with data types
- Monitor device state in real-time
- Support for multiple devices

### Property Control
- Read all device properties with type information
- Write properties with automatic type conversion
- Boolean properties (on/off controls)
- Numeric properties (temperatures, humidity, sensor values)
- Enumerated properties (modes, settings)
- String properties (identifiers, codes)
- Read-only properties (sensors, computed values)

### User Interfaces
- Interactive terminal menu for manual control
- Modern PyQt6-based graphical user interface
- Property editing with intelligent controls
- Real-time device status display

### Home Assistant Integration
- PyScript-based integration for Home Assistant
- Automatic entity creation and management
- Bi-directional synchronization
- Automation support via Home Assistant services

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Setup

```bash
# Clone or download the project
cd tuya_client

# Install required dependencies
pip install -r requirements.txt
```

### Dependencies
- PyQt6 (graphical interface)
- PyYAML (configuration management)
- requests (HTTP communication)
- hashlib (cryptographic signatures)

## Configuration

### Basic Setup

Edit `config.yaml` to configure your Tuya Cloud API credentials:

```yaml
cloud:
  access_id: "your_tuya_api_key"
  access_key: "your_tuya_api_secret"
  region: "eu"

devices:
  - name: "Device Name"
    device_id: "device_uuid_from_tuya"
    type: "Climate"

debug: false
log_level: "INFO"
```

### Obtaining Credentials

1. Visit https://developer.tuya.com/
2. Sign in with your Tuya developer account
3. Create a new project or open existing project
4. Navigate to project settings
5. Copy API Key (access_id) and API Secret (access_key)
6. Identify your region (eu, us, cn, etc.)

### Finding Device IDs

1. Obtain Device UUID from Tuya Developer Platform
2. Alternatively, view in Tuya mobile app device settings
3. Insert into devices list in config.yaml

## Usage

### Command-Line Interface

Launch the interactive terminal menu:

```bash
python tuya_control.py
```

Available options:
1. Display device status
2. List all properties
3. Read single property value
4. Set property value
5. Apply heating scenario
6. Apply cooling scenario
7. Execute custom commands
0. Exit

### Graphical User Interface

Launch the modern GUI application:

```bash
python tuya_gui.py
```

Features:
- Status tab: Device information and current state
- Control tab: Quick controls for common functions
- Properties tab: Interactive editor for all properties
- Configuration tab: View and reference configuration settings

### Python Library

Use as programmatic Python library:

```python
from client import TuyaCloudClient

# Initialize client
client = TuyaCloudClient()
token = client.get_token()

device_id = "your_device_id"

# Get device status
status = client.get_device_status(device_id, token)
print(f"Online: {status.get('is_online')}")

# Retrieve all properties
props = client.get_device_properties(device_id, token)
for code, info in props.items():
    print(f"{code}: {info['value']} ({info['type']})")

# Set property values
client.set_device_property(device_id, token, "Power", True)
client.set_device_property(device_id, token, "temp_set", 220)
client.set_device_property(device_id, token, "mode", "hot")
```

## API Reference

### TuyaCloudClient Class

#### get_token() -> str
Generates a new access token for API communication.

```python
token = client.get_token()
```

#### get_device_status(device_id, token) -> dict
Retrieves device status including online state and network information.

```python
status = client.get_device_status(device_id, token)
is_online = status['is_online']
ip_address = status.get('ip')
```

#### get_device_properties(device_id, token) -> dict
Retrieves all available properties for the device with current values and metadata.

```python
properties = client.get_device_properties(device_id, token)
for code, data in properties.items():
    value = data['value']
    prop_type = data['type']
```

#### get_device_property_value(device_id, token, property_code) -> any
Retrieves a single property value.

```python
current_temperature = client.get_device_property_value(
    device_id, token, "temp_current"
)
```

#### list_device_properties(device_id, token) -> None
Displays formatted table of all device properties.

```python
client.list_device_properties(device_id, token)
```

#### set_device_property(device_id, token, property_code, value) -> bool
Sets a property value to control the device.

```python
# Boolean property
success = client.set_device_property(device_id, token, "Power", True)

# Numeric property (temperature: 220 represents 22 degrees Celsius)
success = client.set_device_property(device_id, token, "temp_set", 220)

# Enumerated property
success = client.set_device_property(device_id, token, "mode", "hot")

# String property
success = client.set_device_property(device_id, token, "setting_code", "value")
```

## Property Catalog

### Common Property Types

| Property Code | Data Type | Description | Example Values |
|---|---|---|---|
| Power | Boolean | Device power state | true, false |
| mode | Enumerated | Operating mode | "hot", "cold", "fan", "dry" |
| temp_set | Numeric | Target temperature (x10) | 160-300 (16-30°C) |
| temp_current | Numeric | Current temperature | varies |
| windspeed | Enumerated | Fan speed level | "auto", "1", "2", "3" |
| humidity_current | Numeric | Current humidity | 0-100 |
| sleep | Enumerated | Sleep mode state | "on", "off" |
| boolCode | String | Device status code | varies |

**Note:** Available properties vary by device type. Use `list_device_properties()` to view all supported properties for your specific device.

## Usage Scenarios

### Scenario 1: Enable Heating Mode

```python
client = TuyaCloudClient()
token = client.get_token()
device_id = "your_device_id"

client.set_device_property(device_id, token, "Power", True)
client.set_device_property(device_id, token, "mode", "hot")
client.set_device_property(device_id, token, "temp_set", 210)
client.set_device_property(device_id, token, "windspeed", "auto")
```

### Scenario 2: Enable Cooling Mode

```python
client.set_device_property(device_id, token, "Power", True)
client.set_device_property(device_id, token, "mode", "cold")
client.set_device_property(device_id, token, "temp_set", 200)
client.set_device_property(device_id, token, "windspeed", "auto")
```

### Scenario 3: Device Shutdown

```python
client.set_device_property(device_id, token, "Power", False)
```

### Scenario 4: Status Monitoring

```python
client = TuyaCloudClient()
token = client.get_token()
device_id = "your_device_id"

props = client.get_device_properties(device_id, token)

print(f"Device: {props.get('name', 'Unknown')}")
print(f"Power: {'On' if props['Power']['value'] else 'Off'}")
print(f"Mode: {props['mode']['value']}")
print(f"Target Temperature: {props['temp_set']['value']/10}°C")
print(f"Current Temperature: {props['temp_current']['value']/10}°C")
print(f"Humidity: {props['humidity_current']['value']}%")
```

## Home Assistant Integration

### PyScript Setup

1. Install PyScript in Home Assistant
2. Add to configuration.yaml:
   ```yaml
   pyscript:
     allow_all_imports: true
   ```
3. Copy `tuya_homeassistant.pyscript` to `/config/pyscript/`
4. Restart Home Assistant

### Available Services

Services are exposed for Home Assistant automations:

- `pyscript.tuya_update_all` - Refresh all entity values from device
- `pyscript.tuya_set_value` - Set a property value
- `pyscript.tuya_create_entities` - Initialize all entities

See `HOMEASSISTANT_SETUP.md` for detailed integration instructions.

## Project Structure

```
tuya_client/
├── client.py                      Core API client library
├── tuya_gui.py                    PyQt6 graphical interface
├── tuya_control.py                Command-line interface
├── launcher.py                    Application launcher
├── config.yaml                    Configuration file
├── tuya_config.yaml               Extended configuration with DP IDs
├── tuya_homeassistant.pyscript   Home Assistant integration
├── requirements.txt               Python dependencies
├── README.md                      This file
├── HOMEASSISTANT_SETUP.md        Home Assistant setup guide
└── start_gui.bat                 Windows GUI launcher
```

## Error Handling

### Token Generation Failure

```python
try:
    token = client.get_token()
    if not token:
        print("Failed to obtain access token")
        exit(1)
except Exception as e:
    print(f"Token error: {e}")
```

### Property Setting Failure

```python
success = client.set_device_property(device_id, token, "Power", True)
if not success:
    print("Failed to set property")
```

### Property Not Found

```python
props = client.get_device_properties(device_id, token)
if "custom_property" not in props:
    print("Property not supported by this device")
```

## Authentication Details

### HMAC-SHA256 Signature

The API uses per-request HMAC-SHA256 signatures for authentication:

```
Signature = HMAC_SHA256(
    client_id + [token +] timestamp + method + content_sha256 + "\n" + path,
    access_key
)
```

All requests include:
- Timestamp (milliseconds)
- Client ID
- Content SHA256 hash
- HMAC-SHA256 signature

### API Endpoint

Cloud API endpoint: `https://openapi.tuyaeu.com/v1.0/iot-03/`

Adjust region in config.yaml (eu, us, cn, etc.)

## Troubleshooting

### Device Not Responding

1. Verify device is online in Tuya app
2. Check device_id is correct in config.yaml
3. Ensure device supports Cloud API control
4. Verify network connectivity

### Authentication Errors

1. Verify Access ID and Access Key in config.yaml
2. Check API credentials in Tuya Developer Platform
3. Ensure credentials have appropriate permissions
4. Verify region setting matches device location

### Property Not Accessible

1. Use `list_device_properties()` to verify property exists
2. Check if property is read-only (cannot be set)
3. Verify value format and type is correct
4. Some properties may require specific device state

### GUI Issues

1. Verify PyQt6 is installed: `pip install PyQt6`
2. Check config.yaml is properly formatted YAML
3. Ensure device_id is valid and accessible
4. Run with debug enabled: set `debug: true` in config.yaml

## Limitations

- Token generation occurs per request (no caching)
- Some devices may be read-only or have restricted properties
- Local device control is not supported
- Only Cloud API is utilized
- Requires active internet connection

## Performance Considerations

- Token generation typically takes 1-2 seconds
- Property reading typically takes 1-3 seconds per device
- Property writing is instantaneous on API side but device response varies
- Bulk operations should batch requests to minimize latency

## Security

- Credentials should never be committed to version control
- Use environment variables or secure config storage in production
- Access keys should have appropriate permission scoping
- HTTPS is used for all API communication
- Signatures are validated per-request

## License

MIT License

## Version History

- Version 1.0 - Initial release (2025-11-25)
  - Full Cloud API implementation
  - PyQt6 GUI application
  - Command-line interface
  - Configuration management
  - Type-aware property handling
