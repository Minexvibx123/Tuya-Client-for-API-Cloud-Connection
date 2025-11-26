#!/usr/bin/env python3
"""
Home Assistant REST API Wrapper for Tuya Client
Provides simple REST endpoints for HA integration

Usage:
  python3 src/tuya_homeassistant_api.py --port 5000

Installation von GitHub (curl):
  # Auf Raspberry Pi / Linux:
  curl -fsSL https://raw.githubusercontent.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/main/install_rest_api.sh | bash
  
  # Oder manuelle Installation:
  cd /root && curl -o tuya_client.tar.gz https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/archive/refs/heads/main.tar.gz
  tar -xzf tuya_client.tar.gz
  cd Tuya-Client-for-API-Cloud-Connection-main
  pip install -r requirements.txt
  python3 src/tuya_homeassistant_api.py --port 5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from client import TuyaCloudClient
import logging

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load configuration
try:
    with open("config.yaml", "r") as f:
        import yaml
        config = yaml.safe_load(f)
except Exception as e:
    _LOGGER.error(f"❌ config.yaml not found. Error: {e}")
    sys.exit(1)

# Initialize client
# Note: TuyaCloudClient expects config.yaml file path
try:
    client = TuyaCloudClient("config.yaml")
except Exception as e:
    _LOGGER.error(f"❌ Failed to initialize TuyaCloudClient: {e}")
    sys.exit(1)

# Get first device from config
devices = config.get("devices", [])
if not devices:
    _LOGGER.error("❌ No devices configured in config.yaml")
    sys.exit(1)

PRIMARY_DEVICE_ID = devices[0].get("device_id")
_LOGGER.info(f"✓ Using device: {devices[0].get('name')} ({PRIMARY_DEVICE_ID})")

# ============================================================
# REST Endpoints for Home Assistant
# ============================================================

@app.route("/status", methods=["GET"])
def get_status():
    """Get current device status"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        status = client.get_device_status(PRIMARY_DEVICE_ID, token)
        return jsonify({
            "success": True,
            "data": status
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/properties", methods=["GET"])
def get_properties():
    """Get all device properties"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        props = client.get_device_properties(PRIMARY_DEVICE_ID, token)
        return jsonify({
            "success": True,
            "data": props
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/property/<property_code>", methods=["GET"])
def get_property(property_code):
    """Get single property"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        props = client.get_device_properties(PRIMARY_DEVICE_ID, token)
        value = props.get(property_code)
        if value is None:
            return jsonify({
                "success": False,
                "error": f"Property {property_code} not found"
            }), 404
        return jsonify({
            "success": True,
            "property": property_code,
            "value": value
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/set", methods=["POST"])
def set_property():
    """Set device property"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        data = request.get_json()
        property_code = data.get("property")
        value = data.get("value")
        
        if not property_code or value is None:
            return jsonify({
                "success": False,
                "error": "Missing property or value"
            }), 400
        
        result = client.set_device_property(PRIMARY_DEVICE_ID, token, property_code, value)
        
        return jsonify({
            "success": result,
            "property": property_code,
            "value": value
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/batch", methods=["POST"])
def batch_set():
    """Set multiple properties at once"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        data = request.get_json()
        properties = data.get("properties", [])
        
        results = {}
        for prop in properties:
            property_code = prop.get("property")
            value = prop.get("value")
            result = client.set_device_property(PRIMARY_DEVICE_ID, token, property_code, value)
            results[property_code] = result
        
        return jsonify({
            "success": True,
            "results": results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/device", methods=["GET"])
def get_device_info():
    """Get device information"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        props = client.get_device_properties(PRIMARY_DEVICE_ID, token)
        info = {
            "device_id": PRIMARY_DEVICE_ID,
            "region": client.region,
            "online": True,
            "properties_count": len(props)
        }
        return jsonify({
            "success": True,
            "data": info
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/schemas", methods=["GET"])
def get_property_schemas():
    """Get all property schemas (types, ranges, enums)"""
    schemas = {
        "boolean": ["Power", "dirty_filter", "freshair_filter", "hot_cold_wind"],
        "numeric": {
            "temp_set": {"min": 160, "max": 300, "step": 10, "unit": "×10°C"},
            "savemoney_temp": {"min": 160, "max": 300, "step": 10, "unit": "×10°C"},
        },
        "enum": {
            "mode": ["cool", "heat", "auto", "wind", "dry"],
            "windspeed": ["low", "mid", "high", "auto"],
            "sleep": ["off", "sleep1", "sleep2", "sleep3"],
            "style": ["manual", "smart"],
            "energy": ["on", "off"],
        },
        "string": {
            "boolCode": {
                "description": "Device status code (DP_ID 123)",
                "readonly": False,
                "examples": ["on", "off", "cooling", "heating", "auto"],
                "note": "Set custom string values to control or display device status"
            },
            "SN_SW_ver": {
                "description": "Serial number and software version",
                "readonly": True
            }
        },
        "readonly": ["temp_current", "humidity_current", "airquality", "pm25", "SN_SW_ver"]
    }
    return jsonify({
        "success": True,
        "schemas": schemas
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    try:
        # Try to get token to verify connection
        token = client.get_token()
        if not token:
            return jsonify({
                "status": "unhealthy",
                "connected": False,
                "error": "Failed to get access token"
            }), 503
        
        # Try to get properties
        props = client.get_device_properties(PRIMARY_DEVICE_ID, token)
        
        if props and isinstance(props, dict):
            return jsonify({
                "status": "healthy",
                "connected": True,
                "properties_count": len(props)
            })
        else:
            return jsonify({
                "status": "unhealthy",
                "connected": False,
                "error": "No properties returned"
            }), 503
    except Exception as e:
        return jsonify({
            "status": "error",
            "connected": False,
            "error": str(e)
        }), 503

# ============================================================
# Home Assistant Integration Endpoint
# ============================================================

@app.route("/boolcode", methods=["GET"])
def get_boolcode():
    """Get boolCode property (DP_ID 123) - String value"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        props = client.get_device_properties(PRIMARY_DEVICE_ID, token)
        boolcode_value = props.get("boolCode")
        
        if boolcode_value is None:
            return jsonify({
                "success": False,
                "error": "boolCode property not found"
            }), 404
        
        return jsonify({
            "success": True,
            "property": "boolCode",
            "value": boolcode_value,
            "type": "string",
            "description": "Device status code (string)"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/boolcode", methods=["POST"])
def set_boolcode():
    """Set boolCode property (DP_ID 123) - String value"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        data = request.get_json()
        value = data.get("value")
        
        if value is None:
            return jsonify({
                "success": False,
                "error": "Missing value parameter"
            }), 400
        
        # Ensure value is string
        value_str = str(value)
        
        result = client.set_device_property(PRIMARY_DEVICE_ID, token, "boolCode", value_str)
        
        return jsonify({
            "success": result,
            "property": "boolCode",
            "value": value_str,
            "type": "string"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route("/api/v1/ha-entities", methods=["GET"])
def ha_entities():
    """Generate Home Assistant entity definitions"""
    try:
        token = client.get_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        props = client.get_device_properties(PRIMARY_DEVICE_ID, token)
        
        entities = {}
        for code, value in props.items():
            entity = {
                "entity_id": f"sensor.tuya_{code}",
                "name": code.replace("_", " ").title(),
                "state": value,
                "attributes": {
                    "friendly_name": code,
                    "icon": _get_icon_for_property(code)
                }
            }
            entities[f"sensor.tuya_{code}"] = entity
        
        return jsonify({
            "success": True,
            "entities": entities,
            "count": len(entities)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

def _get_icon_for_property(property_name):
    """Get appropriate icon for property"""
    icons = {
        "Power": "mdi:power",
        "temp": "mdi:thermometer",
        "humidity": "mdi:water-percent",
        "mode": "mdi:fan",
        "windspeed": "mdi:fan-speed-1",
        "airquality": "mdi:weather-hazy",
        "pm25": "mdi:particle-point",
        "energy": "mdi:lightning-bolt",
        "filter": "mdi:air-filter",
    }
    
    for key, icon in icons.items():
        if key.lower() in property_name.lower():
            return icon
    return "mdi:cog"

# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tuya Client Home Assistant REST API")
    parser.add_argument("--port", type=int, default=5000, help="Port to run on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    args = parser.parse_args()
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  🏠 Tuya Client - Home Assistant REST API                 ║
╠════════════════════════════════════════════════════════════╣
║  Starting on {args.host}:{args.port}
║  
║  Endpoints:
║    GET  /status          - Device status
║    GET  /properties      - All properties
║    GET  /property/<code> - Single property
║    POST /set             - Set property
║    POST /batch           - Set multiple
║    GET  /device          - Device info
║    GET  /schemas         - Property schemas
║    GET  /health          - Health check
║    GET  /boolcode        - Get boolCode (DP_ID 123)
║    POST /boolcode        - Set boolCode (DP_ID 123)
║    GET  /api/v1/ha-entities - HA entities
║
║  Test Endpoint:
║    curl http://{args.host}:{args.port}/health
║
║  boolCode Examples:
║    GET:  curl http://{args.host}:{args.port}/boolcode
║    SET:  curl -X POST http://{args.host}:{args.port}/boolcode \\
║           -H "Content-Type: application/json" \\
║           -d '{{"value":"cooling"}}'
║
║  Other Examples (curl):
║    curl http://{args.host}:{args.port}/properties
║    curl -X POST http://{args.host}:{args.port}/set \\
║      -H "Content-Type: application/json" \\
║      -d '{{"property":"Power", "value":true}}'
║
║  ✓ Health check ready: http://{args.host}:{args.port}/health
╚════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=args.host, port=args.port, debug=False)
