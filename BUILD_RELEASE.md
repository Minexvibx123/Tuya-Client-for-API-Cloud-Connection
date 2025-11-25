# Building Standalone EXE Release

## Quick Start

```bash
python build_simple.py
```

Creates two executables in `dist/`:
- `Tuya-Client-GUI.exe`
- `Tuya-Client-CLI.exe`

## Prerequisites

- Python 3.6+ installed
- `requirements.txt` installed: `pip install -r requirements.txt`
- PyInstaller will auto-install

## Build Methods

### Method 1: Simple Python Script (Recommended)

```bash
python build_simple.py
```

### Method 2: Batch File

```bash
build_exe.bat
```

### Method 3: Manual PyInstaller

```bash
pyinstaller --onefile --windowed tuya_gui.py
pyinstaller --onefile --console tuya_control.py
```

## Output

```
dist/
├── Tuya-Client-GUI.exe      (~40 MB)
├── Tuya-Client-CLI.exe      (~30 MB)
└── config.yaml              (config file)
```

## Release Steps

1. Build: `python build_simple.py`
2. Test the EXEs on a clean system
3. Create ZIP: 
   ```powershell
   Compress-Archive -Path dist -DestinationPath Tuya-Client-Release-v1.0.zip
   ```
4. Upload to GitHub Releases

## Troubleshooting

### Build fails: PyInstaller not found
```bash
pip install pyinstaller
```

### EXE is too large
This is normal (PyQt6 + dependencies = 70+ MB combined)

### "This app cannot run on your PC"
Try rebuilding or install Visual C++ Runtime on target system
