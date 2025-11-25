#!/usr/bin/env python3
"""
Simple Build Script for Tuya Client EXE
Works with PyQt6 and PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_simple():
    """Simple build without problematic PyQt6 hooks"""
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\n" + "="*60)
    print("TUYA CLOUD CLIENT - SIMPLE BUILD")
    print("="*60)
    
    # Clean
    print("\nCleaning...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # Build GUI - minimal options
    print("\nBuilding GUI EXE...")
    gui_cmd = (
        'pyinstaller '
        '--name "Tuya-Client-GUI" '
        '--onefile '
        '--windowed '
        '--add-data "config.yaml:." '
        '--distpath dist '
        'tuya_gui.py'
    )
    
    result = subprocess.run(gui_cmd, shell=True)
    if result.returncode != 0:
        print("GUI build failed!")
        return False
    
    print("✓ GUI built successfully")
    
    # Build CLI
    print("\nBuilding CLI EXE...")
    cli_cmd = (
        'pyinstaller '
        '--name "Tuya-Client-CLI" '
        '--onefile '
        '--console '
        '--add-data "config.yaml:." '
        '--distpath dist '
        'tuya_control.py'
    )
    
    result = subprocess.run(cli_cmd, shell=True)
    if result.returncode != 0:
        print("CLI build failed!")
        return False
    
    print("✓ CLI built successfully")
    
    # Copy configs
    print("\nCopying configuration files...")
    if os.path.exists("config.yaml"):
        shutil.copy("config.yaml", "dist/config.yaml")
    if os.path.exists("tuya_config.yaml"):
        shutil.copy("tuya_config.yaml", "dist/tuya_config.yaml")
    
    print("\n" + "="*60)
    print("BUILD COMPLETED!")
    print("="*60)
    print("\nOutput location:")
    print("  dist/Tuya-Client-GUI.exe")
    print("  dist/Tuya-Client-CLI.exe")
    print("\nNext step: Test the EXE files!")
    
    return True

if __name__ == "__main__":
    success = build_simple()
    sys.exit(0 if success else 1)
