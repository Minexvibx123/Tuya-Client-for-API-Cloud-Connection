#!/usr/bin/env python3
"""
Home Assistant REST API Wrapper for Tuya Client
Provides simple REST endpoints for HA integration

Usage:
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
        API_CONFIG = config["tuya_api"]
except:
    _LOGGER.error("❌ config.yaml not found. Please create it first.")
    sys.exit(1)

# Initialize client
client = TuyaCloudClient(API_CONFIG)

# ============================================================
# REST Endpoints for Home Assistant
# ============================================================

@app.route("/status", methods=["GET"])
def get_status():
    """Get current device status"""
    try:
        status = client.get_device_status()
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
        props = client.get_device_properties()
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
        props = client.get_device_properties()
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
        data = request.get_json()
        property_code = data.get("property")
        value = data.get("value")
        
        if not property_code or value is None:
            return jsonify({
                "success": False,
                "error": "Missing property or value"
            }), 400
        
        result = client.set_device_property(property_code, value)
        
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
        data = request.get_json()
        properties = data.get("properties", [])
        
        results = {}
        for prop in properties:
            property_code = prop.get("property")
            value = prop.get("value")
            result = client.set_device_property(property_code, value)
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
        info = {
            "device_id": client.device_id,
            "region": client.region,
            "online": True,
            "properties_count": len(client.get_device_properties())
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
        if client.get_token():
            return jsonify({
                "status": "healthy",
                "connected": True
            })
        else:
            return jsonify({
                "status": "unhealthy",
                "connected": False
            }), 503
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 503

# ============================================================
# Home Assistant Integration Endpoint
# ============================================================

@app.route("/api/v1/ha-entities", methods=["GET"])
def ha_entities():
    """Generate Home Assistant entity definitions"""
    try:
        props = client.get_device_properties()
        
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
║    GET  /api/v1/ha-entities - HA entities
║
║  Example (curl):
║    curl http://localhost:5000/properties
║    curl -X POST http://localhost:5000/set \\
║      -H "Content-Type: application/json" \\
║      -d '{{"property":"Power", "value":true}}'
╚════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=args.host, port=args.port, debug=False)
