#!/usr/bin/env python3
"""
Tuya Client - Quick EXE Builder
Uses PyInstaller with minimal dependencies
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build():
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\n" + "="*60)
    print("TUYA CLIENT - BUILDING EXECUTABLES")
    print("="*60)
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for item in ["build", "dist", "*.spec"]:
        if "*" in item:
            for f in Path(".").glob(item):
                if f.is_file():
                    f.unlink()
        else:
            if Path(item).exists():
                shutil.rmtree(item)
    
    # Build GUI
    print("\n[1/2] Building GUI Launcher...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "Tuya-Client-GUI",
        "--distpath", "dist",
        "launcher_gui.py"
    ])
    
    if result.returncode != 0:
        print("✗ GUI build failed")
        return False
    print("✓ GUI built")
    
    # Build CLI
    print("\n[2/2] Building CLI Launcher...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "Tuya-Client-CLI",
        "--distpath", "dist",
        "launcher_cli.py"
    ])
    
    if result.returncode != 0:
        print("✗ CLI build failed")
        return False
    print("✓ CLI built")
    
    # Copy config
    print("\nCopying configuration files...")
    if Path("config.yaml").exists():
        shutil.copy("config.yaml", "dist/config.yaml")
        print("✓ config.yaml")
    
    # Summary
    print("\n" + "="*60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    gui_exe = Path("dist/Tuya-Client-GUI.exe")
    cli_exe = Path("dist/Tuya-Client-CLI.exe")
    
    if gui_exe.exists():
        size_mb = gui_exe.stat().st_size / (1024*1024)
        print(f"\n✓ {gui_exe.name} ({size_mb:.1f} MB)")
    
    if cli_exe.exists():
        size_mb = cli_exe.stat().st_size / (1024*1024)
        print(f"✓ {cli_exe.name} ({size_mb:.1f} MB)")
    
    print(f"\nLocation: dist/")
    print("\nTo distribute:")
    print("  1. Copy dist/ folder")
    print("  2. Include config.yaml with credentials")
    print("  3. Create ZIP file for release")
    
    return True

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
