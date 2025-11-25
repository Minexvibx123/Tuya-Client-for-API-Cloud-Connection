# Tuya Cloud Client - Enterprise Edition

Professional Python client library for controlling Tuya Smart Home devices via Tuya Cloud API.

## Quick Start

```bash
# Install dependencies
pip install -r build_output/requirements.txt

# Run GUI
python src/launcher_gui.py

# Run CLI
python src/launcher_cli.py
```

## Build Standalone EXE

```bash
python src/build.py
```

Output: `build_output/release/`

## Project Structure

```
tuya_client/
├── src/                     Source code
│   ├── client.py           Core API client
│   ├── tuya_gui.py         PyQt6 GUI application
│   ├── tuya_control.py     CLI interface
│   ├── launcher_gui.py     GUI launcher
│   ├── launcher_cli.py     CLI launcher
│   ├── build.py            EXE builder
│   └── build_simple.py     Simplified builder
│
├── docs/                    Documentation
│   ├── README.md           Full documentation
│   └── BUILD_RELEASE.md    Build instructions
│
├── config/                  Configuration
│   ├── config.yaml         Basic config (EDIT THIS)
│   └── tuya_config.yaml    Extended config with DP_IDs
│
├── build_output/           Build artifacts
│   ├── release/            Standalone EXEs
│   │   ├── Tuya-Client-GUI.exe
│   │   ├── Tuya-Client-CLI.exe
│   │   └── config.yaml
│   ├── requirements.txt    Python dependencies
│   ├── start_gui.bat       Windows launcher
│   └── start_cli.bat       Windows launcher
│
└── .gitignore             Git configuration
```

## Key Files

| File | Purpose |
|------|---------|
| `src/client.py` | Main Tuya Cloud API client |
| `src/tuya_gui.py` | Modern PyQt6 interface (Status, Control, Properties, Config tabs) |
| `src/tuya_control.py` | Command-line interface for automation |
| `config/config.yaml` | Edit with your Tuya API credentials |
| `docs/README.md` | Complete documentation |
| `build_output/release/` | Standalone EXE files (no Python needed) |

## Configuration

Edit `config/config.yaml`:

```yaml
cloud:
  access_id: "your_api_key"
  access_key: "your_api_secret"
  region: "eu"

devices:
  - name: "Device Name"
    device_id: "your_device_uuid"
    type: "Climate"
```

## Features

- Modern PyQt6 GUI with 4 tabs
- Interactive property editing
- Command-line interface
- Standalone Windows EXEs (no Python installation required)
- Home Assistant integration via PyScript
- Comprehensive configuration management
- All 35+ device properties supported

## Documentation

- **Full Guide**: `docs/README.md`
- **Build Instructions**: `docs/BUILD_RELEASE.md`
- **Home Assistant Setup**: (See main README)

## API Usage

```python
from src.client import TuyaCloudClient

client = TuyaCloudClient()
token = client.get_token()

# Get all properties
props = client.get_device_properties(device_id, token)

# Set a property
client.set_device_property(device_id, token, "Power", True)
```

## Development

1. Clone repository
2. Install requirements: `pip install -r build_output/requirements.txt`
3. Edit `config/config.yaml` with credentials
4. Run: `python src/launcher_gui.py`

## Release

1. Build EXE: `python src/build.py`
2. Test: `build_output/release/Tuya-Client-GUI.exe`
3. Create ZIP: `build_output/release/` folder
4. Upload to GitHub Releases

## License

MIT License

## Repository

https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection
