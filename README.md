# Tuya Cloud Client - Enterprise Edition

[![Python](https://img.shields.io/badge/Python-3.6+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Minexvibx123-white)](https://github.com/Minexvibx123)

Professional Python client library for controlling Tuya Smart Home devices via Tuya Cloud API.

## Features

- ✅ Modern PyQt6 graphical user interface
- ✅ Command-line interface for automation
- ✅ Standalone Windows executables (no Python required)
- ✅ Home Assistant integration via PyScript
- ✅ All 35+ device properties supported
- ✅ Type-aware property handling
- ✅ Complete API documentation

## Quick Start

### Prerequisites
- Python 3.6+
- Windows / Linux / macOS

### Installation

```bash
# Clone repository
git clone https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection.git
cd Tuya-Client-for-API-Cloud-Connection

# Install dependencies
pip install -r build_output/requirements.txt

# Configure your credentials
cp config/config.yaml.example config/config.yaml
# Edit config/config.yaml with your Tuya API credentials
```

### Usage

**GUI Application:**
```bash
python src/launcher_gui.py
```

**CLI Interface:**
```bash
python src/launcher_cli.py
```

**Standalone EXE (Windows):**
```bash
python src/build.py
# Output: build_output/release/Tuya-Client-GUI.exe
```

## Project Structure

```
tuya_client/
├── src/                    Source code
│   ├── client.py          Core API client
│   ├── tuya_gui.py        PyQt6 GUI application
│   ├── tuya_control.py    CLI interface
│   ├── launcher_gui.py    GUI launcher
│   └── build.py           EXE builder
│
├── docs/                   Documentation
│   ├── README.md          Full guide
│   └── BUILD_RELEASE.md   Build instructions
│
├── config/                Configuration (gitignored)
│   ├── config.yaml.example         Template
│   └── tuya_config.yaml.example    Advanced template
│
├── build_output/           Build artifacts
│   ├── release/           Standalone EXEs
│   └── requirements.txt    Dependencies
│
└── .github/               GitHub configuration
    └── workflows/         CI/CD workflows
```

## Configuration

Copy and edit `config/config.yaml`:

```yaml
cloud:
  access_id: "your_tuya_api_key"
  access_key: "your_tuya_api_secret"
  region: "eu"  # eu, us, cn, etc.

devices:
  - name: "Your Device"
    device_id: "your_device_uuid"
    type: "Climate"
```

Get credentials from: https://developer.tuya.com/

## GUI Features

### Status Tab
- Device online/offline status
- Current and target temperatures
- Operating mode
- Wind speed
- Humidity and air quality

### Control Tab
- Power on/off
- Mode selection (heat/cold/fan/dry)
- Temperature adjustment
- Wind speed control

### Properties Tab
- All 35+ properties with interactive editing
- Type-aware controls (toggles, sliders, dropdowns)
- Read-only sensor displays
- Live updates

### Configuration Tab
- View API configuration
- Display connected devices
- Debug settings reference

## API Usage

```python
from src.client import TuyaCloudClient

client = TuyaCloudClient()
token = client.get_token()
device_id = "your_device_id"

# Get device status
status = client.get_device_status(device_id, token)
print(f"Online: {status['is_online']}")

# Get all properties
props = client.get_device_properties(device_id, token)
for code, info in props.items():
    print(f"{code}: {info['value']}")

# Set property
client.set_device_property(device_id, token, "Power", True)
client.set_device_property(device_id, token, "temp_set", 220)  # 22°C
```

## Building Standalone EXE

```bash
# Ensure all requirements are installed
pip install -r build_output/requirements.txt

# Build both GUI and CLI executables
python src/build.py

# Output:
# - build_output/release/Tuya-Client-GUI.exe (41 MB)
# - build_output/release/Tuya-Client-CLI.exe (14 MB)
```

For detailed build instructions, see [BUILD_RELEASE.md](docs/BUILD_RELEASE.md)

## Documentation

- **Full Documentation**: [docs/README.md](docs/README.md)
- **Build Guide**: [docs/BUILD_RELEASE.md](docs/BUILD_RELEASE.md)
- **API Reference**: See [docs/README.md](docs/README.md#api-reference)

## Technology Stack

- **GUI**: PyQt6
- **HTTP**: requests
- **Config**: PyYAML
- **Crypto**: HMAC-SHA256
- **Build**: PyInstaller

## Supported Devices

- Tuya Climate Control (Smart Thermostats)
- Fresh Air Systems
- Smart HVAC Units
- Other Tuya Cloud API compatible devices

35+ device properties supported with full type system:
- Boolean properties (on/off)
- Numeric values (temperatures, humidity, etc.)
- Enumerated settings (modes, speeds, etc.)
- String identifiers (codes, serials)
- Read-only sensors

## Home Assistant Integration

PyScript integration available for Home Assistant. See [HOMEASSISTANT_SETUP.md](docs/HOMEASSISTANT_SETUP.md) for setup instructions.

## Performance

- Token generation: ~1-2 seconds
- Property read: ~1-3 seconds
- Property write: Instantaneous (API side)
- GUI startup: ~2-3 seconds
- EXE startup: ~2-3 seconds

## Troubleshooting

### "Connection refused" Error
- Verify device is online in Tuya app
- Check device_id is correct
- Ensure device supports Cloud API
- Verify network connectivity

### "type is incorrect" Error
- Property type mismatch
- Use type-aware parsing (handled automatically)
- Check property format in config

### GUI Won't Start
- Verify PyQt6 is installed: `pip install PyQt6`
- Check config.yaml is valid YAML
- Ensure credentials are correct

### Build Fails
- Install PyInstaller: `pip install pyinstaller`
- Check Python version (3.6+)
- Verify all dependencies installed

## Development

```bash
# Clone and setup
git clone https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection.git
cd Tuya-Client-for-API-Cloud-Connection
pip install -r build_output/requirements.txt

# Run directly
python src/launcher_gui.py

# Run CLI
python src/launcher_cli.py
```

## Release Process

1. Test application thoroughly
2. Update version in docs
3. Build EXE: `python src/build.py`
4. Create ZIP: `build_output/release/`
5. Create GitHub Release
6. Upload EXE ZIP as asset

## License

MIT License - See [LICENSE](LICENSE)

## Author

- **Minexvibx123** - [GitHub Profile](https://github.com/Minexvibx123)

## Repository

https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection

## Support

For issues and questions:
- GitHub Issues: https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/issues
- Discussions: https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/discussions

## Changelog

### v1.0 (Latest)
- Initial release
- PyQt6 GUI with 4 tabs
- Standalone EXE support
- Home Assistant integration
- All 35+ device properties

---

**Last Updated**: November 25, 2025
