#!/usr/bin/env python3
"""
Tuya Client CLI Launcher
Lightweight wrapper for CLI interface
"""

import sys
import os

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Launch CLI
if __name__ == "__main__":
    from tuya_control import main
    main()
