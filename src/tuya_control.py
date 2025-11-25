#!/usr/bin/env python3
"""
TUYA CLOUD CLIENT - FINALES UNIVERSELLES SKRIPT
Lesen + Schreiben von Tuya Smart Home Geräten über Cloud API
"""

from client import TuyaCloudClient
import yaml
import sys
import time


def load_config():
    """Lädt config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ config.yaml nicht gefunden!")
        sys.exit(1)


def print_menu():
    """Zeigt Hauptmenü"""
    print("\n" + "=" * 80)
    print("TUYA CLOUD CLIENT - HAUPTMENÜ")
    print("=" * 80)
    print("""
[1] Device Status anzeigen
[2] Alle Properties auflisten
[3] Einzelne Property auslesen
[4] Property setzen (Gerät steuern)
[5] Schneltszenario: Heizen auf 21°C
[6] Schneltszenario: Kühlen auf 20°C
[7] Custom Command
[0] Beenden

""")


def show_device_status(client, device_id, token):
    """Zeigt Gerätestatus"""
    print("\n" + "=" * 80)
    print("GERÄTESTATUS")
    print("=" * 80)
    
    status = client.get_device_status(device_id, token)
    
    print(f"""
Name:          {status.get('name')}
ID:            {status.get('id')}
Online:        {'🟢 ONLINE' if status.get('is_online') else '🔴 OFFLINE'}
IP:            {status.get('ip')}
Kategorie:     {status.get('category')}
Produkt:       {status.get('product_name')}
Zeitzone:      {status.get('time_zone')}
Lokaler Key:   {status.get('local_key')}
""")


def list_all_properties(client, device_id, token):
    """Listet alle Properties auf"""
    print("\n" + "=" * 80)
    print("ALLE PROPERTIES")
    print("=" * 80)
    
    client.list_device_properties(device_id, token)


def read_single_property(client, device_id, token):
    """Liest einzelne Property"""
    print("\n" + "=" * 80)
    print("PROPERTY AUSLESEN")
    print("=" * 80)
    
    # Zeige verfügbare Properties
    props = client.get_device_properties(device_id, token)
    codes = sorted(props.keys())
    
    print("\nVerfügbare Properties:")
    for i, code in enumerate(codes, 1):
        value = props[code]['value']
        print(f"  [{i:2d}] {code:25} = {value}")
    
    try:
        idx = int(input("\nWähle Property (Nummer): ")) - 1
        if 0 <= idx < len(codes):
            code = codes[idx]
            value = client.get_device_property_value(device_id, token, code)
            print(f"\n✓ {code} = {value}")
        else:
            print("❌ Ungültige Auswahl")
    except ValueError:
        print("❌ Bitte Zahl eingeben")


def set_property(client, device_id, token):
    """Setzt Property"""
    print("\n" + "=" * 80)
    print("PROPERTY SETZEN")
    print("=" * 80)
    
    # Zeige verfügbare Properties
    props = client.get_device_properties(device_id, token)
    codes = sorted(props.keys())
    
    print("\nVerfügbare Properties:")
    for i, code in enumerate(codes, 1):
        prop_type = props[code].get('type', 'unknown')
        value = props[code]['value']
        print(f"  [{i:2d}] {code:25} (Type: {prop_type:10}) = {value}")
    
    try:
        idx = int(input("\nWähle Property (Nummer): ")) - 1
        if 0 <= idx < len(codes):
            code = codes[idx]
            prop_type = props[code].get('type', 'unknown')
            
            # Eingabe basierend auf Type
            if prop_type == 'bool':
                val_input = input(f"Neuer Wert (true/false): ").lower()
                value = val_input in ['true', '1', 'yes', 'ja']
            elif prop_type == 'enum':
                value = input(f"Neuer Wert (enum): ")
            elif prop_type == 'value':
                value = int(input(f"Neuer Wert (Zahl): "))
            else:
                value = input(f"Neuer Wert: ")
            
            # Setzen
            result = client.set_device_property(device_id, token, code, value)
            if result:
                print(f"✓ {code} auf {value} gesetzt!")
                
                # Status überprüfen
                time.sleep(1)
                new_value = client.get_device_property_value(device_id, token, code)
                print(f"✓ Bestätigung: {code} = {new_value}")
            else:
                print(f"❌ Fehler beim Setzen von {code}")
        else:
            print("❌ Ungültige Auswahl")
    except ValueError as e:
        print(f"❌ Fehler: {e}")


def scenario_heating(client, device_id, token):
    """Szenario: Heizen auf 21°C"""
    print("\n" + "=" * 80)
    print("SZENARIO: HEIZEN (21°C)")
    print("=" * 80)
    
    print("\n→ Konfiguriere Device...")
    
    client.set_device_property(device_id, token, "Power", True)
    print("  ✓ Power: ON")
    
    client.set_device_property(device_id, token, "mode", "hot")
    print("  ✓ Mode: Heating")
    
    client.set_device_property(device_id, token, "temp_set", 210)
    print("  ✓ Temperature: 21°C")
    
    client.set_device_property(device_id, token, "windspeed", "auto")
    print("  ✓ Windspeed: Auto")
    
    # Status anzeigen
    time.sleep(2)
    props = client.get_device_properties(device_id, token)
    
    print("\n→ Aktueller Status:")
    print(f"  Power:        {props['Power']['value']}")
    print(f"  Mode:         {props['mode']['value']}")
    print(f"  Set Temp:     {props['temp_set']['value'] / 10}°C")
    print(f"  Current Temp: {props['temp_current']['value']}°C")
    print(f"  Windspeed:    {props['windspeed']['value']}")


def scenario_cooling(client, device_id, token):
    """Szenario: Kühlen auf 20°C"""
    print("\n" + "=" * 80)
    print("SZENARIO: KÜHLEN (20°C)")
    print("=" * 80)
    
    print("\n→ Konfiguriere Device...")
    
    client.set_device_property(device_id, token, "Power", True)
    print("  ✓ Power: ON")
    
    client.set_device_property(device_id, token, "mode", "cold")
    print("  ✓ Mode: Cooling")
    
    client.set_device_property(device_id, token, "temp_set", 200)
    print("  ✓ Temperature: 20°C")
    
    client.set_device_property(device_id, token, "windspeed", "auto")
    print("  ✓ Windspeed: Auto")
    
    # Status anzeigen
    time.sleep(2)
    props = client.get_device_properties(device_id, token)
    
    print("\n→ Aktueller Status:")
    print(f"  Power:        {props['Power']['value']}")
    print(f"  Mode:         {props['mode']['value']}")
    print(f"  Set Temp:     {props['temp_set']['value'] / 10}°C")
    print(f"  Current Temp: {props['temp_current']['value']}°C")
    print(f"  Windspeed:    {props['windspeed']['value']}")


def custom_command(client, device_id, token):
    """Custom Command"""
    print("\n" + "=" * 80)
    print("CUSTOM COMMAND")
    print("=" * 80)
    
    prop_code = input("\nProperty Code: ").strip()
    prop_value = input("Property Value: ").strip()
    
    # Versuche Value zu parsen
    try:
        if prop_value.lower() in ['true', 'false']:
            value = prop_value.lower() == 'true'
        else:
            try:
                value = int(prop_value)
            except:
                value = prop_value
    except:
        value = prop_value
    
    result = client.set_device_property(device_id, token, prop_code, value)
    if result:
        print(f"\n✓ {prop_code} = {value} gesetzt!")
    else:
        print(f"\n❌ Fehler beim Setzen von {prop_code}")


def main():
    """Hauptprogramm"""
    config = load_config()
    device_id = config['devices'][0]['device_id']
    
    print("\n" + "=" * 80)
    print("TUYA CLOUD CLIENT GESTARTET")
    print("=" * 80)
    print(f"\nGeräte: {config['devices'][0]['name']}")
    print(f"Device ID: {device_id}")
    print(f"Region: {config['cloud']['region']}")
    
    # Client
    client = TuyaCloudClient()
    token = client.get_token()
    
    if not token:
        print("\n❌ Token-Generierung fehlgeschlagen!")
        sys.exit(1)
    
    print(f"✓ Token erhalten\n")
    
    # Hauptschleife
    while True:
        print_menu()
        
        choice = input("Wähle Option: ").strip()
        
        if choice == "1":
            show_device_status(client, device_id, token)
        elif choice == "2":
            list_all_properties(client, device_id, token)
        elif choice == "3":
            read_single_property(client, device_id, token)
        elif choice == "4":
            set_property(client, device_id, token)
        elif choice == "5":
            scenario_heating(client, device_id, token)
        elif choice == "6":
            scenario_cooling(client, device_id, token)
        elif choice == "7":
            custom_command(client, device_id, token)
        elif choice == "0":
            print("\n👋 Auf Wiedersehen!\n")
            break
        else:
            print("\n❌ Ungültige Option")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programm beendet (Ctrl+C)\n")
    except Exception as e:
        print(f"\n❌ Fehler: {e}\n")
        import traceback
        traceback.print_exc()
