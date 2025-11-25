#!/usr/bin/env python3
"""
Tuya Cloud Client - Saubere Implementation
Offizielle API: https://developer.tuya.com/en/docs/iot/new-singnature?id=Kbw0q34cs2e5g
"""

import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import logging
import yaml
import json
import time
import hmac
import hashlib
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class TuyaCloudClient:
    """Tuya Cloud Client mit offiziellem Authentication"""
    
    def __init__(self, config_file: str = "config.yaml"):
        """Initialisiert Client mit Config"""
        self.config = self._load_config(config_file)
        
        # Credentials
        self.access_id = self.config.get('cloud', {}).get('access_id')
        self.access_key = self.config.get('cloud', {}).get('access_key')
        self.region = self.config.get('cloud', {}).get('region', 'eu')
        self.base_url = f"https://openapi.tuya{self.region}.com"
        
        # Device list
        self.devices = {}
        for device in self.config.get('devices', []):
            device_id = device.get('device_id')
            self.devices[device_id] = device
        
        logger.info(f"Tuya Client initialisiert - Region: {self.region}")
        logger.info(f"Geräte: {len(self.devices)}")
    
    def _load_config(self, path: str) -> Dict:
        """Lädt YAML Config"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Config Error: {e}")
            return {}
    
    def _sha256(self, data: str) -> str:
        """SHA256 Hash"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def _generate_signature(self,
                           method: str,
                           path: str,
                           body: Optional[str] = None,
                           access_token: Optional[str] = None) -> tuple:
        """
        Generiert Signature nach Tuya Docs
        
        Basiert auf: https://github.com/jasonacox/tinytuya/blob/master/tinytuya/Cloud.py
        
        Zurückgegeben: (signature, timestamp)
        """
        timestamp = int(time.time() * 1000)
        
        # Basis Payload: client_id + [access_token +] timestamp
        if access_token:
            payload = self.access_id + access_token + str(timestamp)
        else:
            payload = self.access_id + str(timestamp)
        
        # Neue Signatur-Methode (new_sign_algorithm=True):
        # Berechne Content-SHA256
        content_sha256 = self._sha256(body) if body else self._sha256("")
        
        # Vollständige stringToSign:
        # HTTPMethod + "\n" +
        # Content-SHA256 + "\n" +
        # Headers + "\n" +
        # Path
        string_to_sign = f"{method}\n{content_sha256}\n\n{path}"
        
        # Gesamter zu signierter String
        payload += string_to_sign
        
        logger.debug(f"Payload to sign:\n{payload}")
        
        # HMAC-SHA256
        signature = hmac.new(
            self.access_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
        
        return signature, str(timestamp)
    
    def _request(self,
                method: str,
                path: str,
                body: Optional[Dict] = None,
                access_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Macht HTTP Request mit Signature (wie tinytuya)
        """
        url = self.base_url + path
        body_str = json.dumps(body, separators=(',', ':')) if body else ""
        
        # Generiere Signature
        signature, timestamp = self._generate_signature(
            method, path, body_str, access_token
        )
        
        # Headers
        headers = {
            "sign_method": "HMAC-SHA256",
            "client_id": self.access_id,
            "t": timestamp,
            "sign": signature,
            "Content-Type": "application/json",
        }
        
        if access_token:
            headers["access_token"] = access_token
        
        logger.debug(f"{method} {path}")
        logger.debug(f"Headers: {headers}")
        
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                resp = requests.post(url, headers=headers, data=body_str, timeout=10)
            else:
                return {"success": False, "msg": f"Unsupported method: {method}"}
            
            logger.debug(f"Status: {resp.status_code}")
            result = resp.json()
            logger.debug(f"Response: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Request Error: {e}")
            return {"success": False, "msg": str(e)}
    
    def get_token(self) -> Optional[str]:
        """
        Holt Access Token
        
        API: GET /v1.0/token?grant_type=1
        """
        logger.info("Hole Access Token...")
        result = self._request("GET", "/v1.0/token?grant_type=1")
        
        # Token ist in result['result']['access_token']
        if result.get("success") and "result" in result:
            token = result["result"].get("access_token")
            if token:
                logger.info(f"✓ Token erhalten: {token[:20]}...")
                return token
        
        logger.error(f"✗ Token Error: {result.get('msg')}")
        return None
    
    def get_device_status(self, device_id: str, token: str) -> Dict[str, Any]:
        """
        Holt Device Status
        
        API: GET /v2.0/cloud/thing/batch?device_ids={id}
        """
        path = f"/v2.0/cloud/thing/batch?device_ids={device_id}"
        result = self._request("GET", path, access_token=token)
        
        if result.get("success"):
            devices = result.get("result", [])
            if devices:
                return devices[0]
        
        logger.error(f"Status Error: {result.get('msg')}")
        return {}
    
    def get_device_properties(self, device_id: str, token: str) -> Dict[str, Any]:
        """
        Holt alle Device Properties mit aktuellen Werten
        
        API: GET /v2.0/cloud/thing/{device_id}/shadow/properties
        """
        path = f"/v2.0/cloud/thing/{device_id}/shadow/properties"
        result = self._request("GET", path, access_token=token)
        
        if result.get("success") and "result" in result:
            properties = result["result"].get("properties", [])
            
            # Strukturiere Properties für einfache Verwendung
            props_dict = {}
            for prop in properties:
                code = prop.get("code")
                value = prop.get("value")
                props_dict[code] = {
                    "code": code,
                    "dp_id": prop.get("dp_id"),
                    "type": prop.get("type"),
                    "value": value,
                    "time": prop.get("time"),
                    "custom_name": prop.get("custom_name")
                }
            
            return props_dict
        
        logger.error(f"Properties Error: {result.get('msg')}")
        return {}
    
    def get_device_property_value(self, device_id: str, token: str, property_code: str) -> Any:
        """
        Holt einen einzelnen Property-Wert
        
        Args:
            device_id: Device ID
            token: Access Token
            property_code: Property Code (z.B. 'temp_current', 'Power', etc.)
        
        Returns:
            Property-Wert oder None
        """
        properties = self.get_device_properties(device_id, token)
        if property_code in properties:
            return properties[property_code].get("value")
        
        logger.warning(f"Property '{property_code}' nicht gefunden")
        return None
    
    def list_device_properties(self, device_id: str, token: str) -> None:
        """
        Zeigt alle verfügbaren Properties eines Geräts an
        """
        properties = self.get_device_properties(device_id, token)
        
        if not properties:
            print("Keine Properties gefunden")
            return
        
        print(f"\n{'Code':<25} {'Type':<10} {'Value':<20} {'DP_ID':<5}")
        print("-" * 70)
        
        for code, prop in sorted(properties.items()):
            prop_type = prop.get("type", "unknown")
            value = prop.get("value", "-")
            dp_id = prop.get("dp_id", "-")
            
            # Formatiere Value für Anzeige
            if isinstance(value, str) and len(value) > 17:
                value = value[:17] + ".."
            
            print(f"{code:<25} {prop_type:<10} {str(value):<20} {dp_id:<5}")
    
    def set_device_property(self, device_id: str, token: str,
                          property_code: str, value: Any) -> bool:
        """
        Setzt Device Property über Command API
        
        API: POST /v1.0/iot-03/devices/{device_id}/commands
        
        Verwendet property_code (nicht DP_ID!)
        """
        # Validiere dass Property existiert
        properties = self.get_device_properties(device_id, token)
        
        if property_code not in properties:
            logger.error(f"Property '{property_code}' nicht gefunden")
            return False
        
        # Verwende tinytuya Command API Format
        path = f"/v1.0/iot-03/devices/{device_id}/commands"
        body = {
            "commands": [
                {"code": property_code, "value": value}
            ]
        }
        
        result = self._request("POST", path, body, access_token=token)
        
        if result.get("success"):
            logger.info(f"✓ Property '{property_code}' gesetzt auf {value}")
            return True
        else:
            logger.error(f"Property Error: {result.get('msg')}")
            return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TUYA CLOUD CLIENT - SAUBERE IMPLEMENTATION")
    print("="*70 + "\n")
    
    try:
        # Initialisiere Client
        client = TuyaCloudClient()
        
        # Hole Token
        token = client.get_token()
        if not token:
            print("✗ Konnte Token nicht abrufen")
            sys.exit(1)
        
        # Teste Device Status
        print("\n[Test] Device Status:")
        for device_id, device_info in client.devices.items():
            name = device_info.get('name', device_id)
            print(f"\n  Gerät: {name}")
            status = client.get_device_status(device_id, token)
            
            if status:
                print(f"    Online: {status.get('is_online')}")
                print(f"    IP: {status.get('ip')}")
            else:
                print(f"    Fehler beim Abrufen des Status")
        
        print("\n" + "="*70)
        print("✓ Saubere Implementation funktioniert!")
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"✗ Fehler: {e}")
        import traceback
        traceback.print_exc()
