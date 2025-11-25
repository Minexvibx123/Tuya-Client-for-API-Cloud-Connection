#!/usr/bin/env python3
"""
Tuya Client GUI Launcher
Lightweight wrapper for PyQt6 GUI
"""

import sys
import os

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Launch GUI
if __name__ == "__main__":
    from tuya_gui import main
    main()
