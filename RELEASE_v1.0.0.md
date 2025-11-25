# Tuya Cloud Client v1.0.0 - Release Notes

**Release Date:** November 25, 2025  
**Status:** Production Ready ✅

## What's Included

### Standalone Executables (No Python Required)
- `Tuya-Client-GUI.exe` (41.7 MB) - Modern graphical interface
- `Tuya-Client-CLI.exe` (14.3 MB) - Command-line interface

### Features
- ✅ PyQt6 GUI with 4 tabs (Status, Control, Properties, Config)
- ✅ Interactive property editing for all 35+ device properties
- ✅ Type-aware controls (toggles, sliders, dropdowns)
- ✅ Command-line interface for automation
- ✅ Standalone executables (Windows)
- ✅ Home Assistant PyScript integration
- ✅ Comprehensive device support

### Device Support
- Fresh air systems
- Smart thermostats
- HVAC units
- Climate control devices
- 35+ property types

## Installation

### Option 1: Download Standalone (Recommended for Users)
1. Download `Tuya-Client-v1.0.0-Release.zip`
2. Extract to your desired location
3. Edit `config.yaml` with your Tuya API credentials
4. Run `Tuya-Client-GUI.exe` or `Tuya-Client-CLI.exe`

### Option 2: Development (For Developers)
```bash
git clone https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection.git
cd Tuya-Client-for-API-Cloud-Connection
pip install -r build_output/requirements.txt
python src/launcher_gui.py
```

## Configuration

1. Get API credentials from https://developer.tuya.com/
2. Edit `config.yaml`:
   ```yaml
   cloud:
     access_id: "your_api_key"
     access_key: "your_api_secret"
     region: "eu"
   
   devices:
     - name: "Your Device"
       device_id: "your_device_uuid"
   ```

## GUI Overview

### Status Tab
- Device online/offline status
- Current temperature & humidity
- Operating mode
- Air quality metrics

### Control Tab
- Power on/off
- Mode selection (heat/cool/fan/dry)
- Temperature control
- Fan speed adjustment

### Properties Tab
- All 35+ device properties
- Interactive editing
- Read-only sensor display
- Real-time updates

### Configuration Tab
- API settings reference
- Device information
- Debug configuration

## System Requirements

### For Standalone EXE
- Windows 7 or later
- No Python installation required
- ~60 MB disk space

### For Development
- Python 3.6+
- PyQt6, requests, PyYAML
- ~100 MB disk space with dependencies

## Key Improvements in v1.0

1. **PyInstaller Compatibility Fix** - Resolved sys.stdout encoding issues
2. **Professional Structure** - Organized into src/, docs/, config/, build_output/
3. **Standalone EXEs** - Working Windows executables with no Python dependency
4. **Enhanced Documentation** - Complete README with API reference
5. **Configuration Templates** - Example files for safe configuration
6. **CI/CD Workflow** - GitHub Actions for automated testing

## Known Limitations

- Local device control not supported (Cloud API only)
- Some devices may be read-only
- Home Assistant integration requires PyScript addon
- Requires active internet connection

## Support & Documentation

- **Full Documentation:** [docs/README.md](docs/README.md)
- **Build Instructions:** [docs/BUILD_RELEASE.md](docs/BUILD_RELEASE.md)
- **GitHub Issues:** https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/issues
- **GitHub Discussions:** https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/discussions

## File Structure

```
Tuya-Client-v1.0.0/
├── Tuya-Client-GUI.exe       GUI application
├── Tuya-Client-CLI.exe       CLI application
├── config.yaml               Configuration (EDIT THIS)
└── README.txt                Quick start guide
```

## Building from Source

```bash
python src/build.py
```

Output: `build_output/release/`

## License

MIT License - Free to use and modify

## Version History

### v1.0.0 (Current)
- Initial public release
- Full GUI with PyQt6
- Standalone executables
- 35+ device properties
- Home Assistant integration ready

### Future Roadmap
- [ ] macOS support
- [ ] Linux support
- [ ] PyPI package
- [ ] Home Assistant addon
- [ ] Web interface

## Credits

- **Author:** Minexvibx123
- **API:** Tuya Cloud API
- **Framework:** PyQt6
- **Build:** PyInstaller

## Download

**Latest Release:** v1.0.0  
**Download:** [Tuya-Client-v1.0.0-Release.zip](https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/releases/download/v1.0.0/Tuya-Client-v1.0.0-Release.zip)

---

**Questions?** Open an issue on GitHub!
