# Home Assistant Konfiguration - Praktische Beispiele

## Schnellstart (3 Schritte)

### 1. PyScript-Datei kopieren

```
config/pyscript/tuya_client.py
```

### 2. Credentials eintragen

```python
TUYA_ACCESS_ID = "deine_access_id"
TUYA_ACCESS_KEY = "deine_access_key"
TUYA_DEVICE_ID = "deine_device_id"
```

### 3. Home Assistant neu starten

Fertig! Services sind dann unter `pyscript.tuya_*` verfügbar.

---

## Konfigurations-Vorlagen

### A) Input Helpers (helpers.yaml)

```yaml
input_boolean:
  tuya_power:
    name: "Tuya Power"
    icon: mdi:power

input_number:
  tuya_temp_set:
    name: "Set Temperature"
    min: 160
    max: 300
    step: 10
    unit_of_measurement: "×10°C"
    icon: mdi:thermometer

input_select:
  tuya_mode:
    name: "Mode"
    options:
      - "cool"
      - "heat"
      - "auto"
      - "wind"
      - "dry"
```

### B) Automationen (automations.yaml)

```yaml
# Automation 1: Power via Dashboard
- id: tuya_power_control
  alias: "Tuya: Power Steuerung"
  description: "Steuere Power über Input Boolean"
  trigger:
    platform: state
    entity_id: input_boolean.tuya_power
  condition: []
  action:
    - service: pyscript.tuya_set_property
      data:
        property_code: "Power"
        value: "{{ trigger.to_state.state == 'on' }}"

# Automation 2: Temperatur Auto-Erhöhung
- id: tuya_auto_heat
  alias: "Tuya: Auto Heizen wenn kalt"
  trigger:
    platform: numeric_state
    entity_id: sensor.tuya_temp_current
    below: 18
  action:
    - service: pyscript.tuya_set_property
      data:
        property_code: "mode"
        value: "hot"
    - service: pyscript.tuya_set_property
      data:
        property_code: "temp_set"
        value: 220

# Automation 3: Nachts ausschalten
- id: tuya_night_off
  alias: "Tuya: Nachts ausschalten"
  trigger:
    platform: time
    at: "23:00:00"
  action:
    - service: pyscript.tuya_set_property
      data:
        property_code: "Power"
        value: false
    - service: notify.mobile_app
      data:
        message: "Tuya Gerät ausgeschaltet"

# Automation 4: Morgens einschalten
- id: tuya_morning_on
  alias: "Tuya: Morgens einschalten"
  trigger:
    platform: time
    at: "06:00:00"
  condition:
    - condition: state
      entity_id: binary_sensor.workday
      state: "on"
  action:
    - service: pyscript.tuya_set_property
      data:
        property_code: "Power"
        value: true
    - service: pyscript.tuya_set_property
      data:
        property_code: "mode"
        value: "auto"

# Automation 5: Benachrichtigung bei hohem PM2.5
- id: tuya_air_quality_alert
  alias: "Tuya: Luftqualitäts-Alert"
  trigger:
    platform: numeric_state
    entity_id: sensor.tuya_pm25
    above: 100
  action:
    - service: notify.mobile_app_user_phone
      data:
        message: "⚠️ Hohe PM2.5: {{ states('sensor.tuya_pm25') }}"
        title: "Luftqualität kritisch"
```

### C) Template Sensoren (template.yaml)

```yaml
sensor:
  - platform: template
    sensors:
      tuya_temperature_celsius:
        friendly_name: "Temperatur (°C)"
        unique_id: tuya_temp_c
        unit_of_measurement: "°C"
        state: "{{ ((states('sensor.tuya_temp_current') | int(0)) / 10) | round(1) }}"
      
      tuya_temperature_fahrenheit:
        friendly_name: "Temperatur (°F)"
        unique_id: tuya_temp_f
        unit_of_measurement: "°F"
        state: "{{ (((states('sensor.tuya_temp_current') | int(0)) / 10) * 1.8 + 32) | round(1) }}"
      
      tuya_air_quality_text:
        friendly_name: "Luftqualität"
        unique_id: tuya_air_quality
        state: >
          {% set aq = states('sensor.tuya_airquality') | int(0) %}
          {% if aq <= 2 %} Excellent
          {% elif aq <= 4 %} Good
          {% elif aq <= 6 %} Fair
          {% elif aq <= 8 %} Poor
          {% else %} Very Poor
          {% endif %}
      
      tuya_filter_status:
        friendly_name: "Filter-Status"
        unique_id: tuya_filter_status
        icon_template: >
          {% if states('sensor.tuya_dirty_filter') == 'on' %} mdi:alert
          {% else %} mdi:check-circle
          {% endif %}
        state: >
          {% if states('sensor.tuya_dirty_filter') == 'on' %} Wechsel nötig
          {% else %} OK
          {% endif %}
```

---

## Dashboard-Beispiele (Lovelace)

### 1) Einfaches Dashboard

```yaml
title: Tuya Control
views:
  - title: Übersicht
    path: tuya
    cards:
      - type: vertical-stack
        cards:
          # Hauptschalter
          - type: custom:button-card
            name: Power
            entity: input_boolean.tuya_power
            state_color: true
            size: 50%
          
          # Temperatur-Anzeige
          - type: gauge
            entity: sensor.tuya_temp_current
            min: 10
            max: 30
            needle: true
          
          # Luftqualität
          - type: entity
            entity: sensor.tuya_air_quality_text
          
          # Mode Selection
          - type: entities
            entities:
              - entity: input_select.tuya_mode
                name: "Betriebsart"
              - entity: input_select.tuya_windspeed
                name: "Lüftergeschwindigkeit"
```

### 2) Professionelles Dashboard

```yaml
title: Tuya Device Control
views:
  - title: Status
    path: status
    icon: mdi:information
    cards:
      - type: vertical-stack
        cards:
          - type: markdown
            content: |
              # 🌡️ Tuya Device Status
          
          - type: grid
            columns: 2
            cards:
              - type: stat-graph
                entity: sensor.tuya_temp_current
                period: hour
              
              - type: stat-graph
                entity: sensor.tuya_humidity_current
                period: hour
              
              - type: gauge
                entity: sensor.tuya_pm25
              
              - type: gauge
                entity: sensor.tuya_airquality
  
  - title: Controls
    path: controls
    icon: mdi:remote
    cards:
      - type: vertical-stack
        cards:
          - type: custom:button-card
            name: Power
            entity: input_boolean.tuya_power
            tap_action:
              action: toggle
            size: 100px
          
          - type: horizontal-stack
            cards:
              - type: custom:button-card
                name: Heat
                tap_action:
                  action: call-service
                  service: pyscript.tuya_set_property
                  data:
                    property_code: "mode"
                    value: "hot"
              
              - type: custom:button-card
                name: Cool
                tap_action:
                  action: call-service
                  service: pyscript.tuya_set_property
                  data:
                    property_code: "mode"
                    value: "cool"
              
              - type: custom:button-card
                name: Auto
                tap_action:
                  action: call-service
                  service: pyscript.tuya_set_property
                  data:
                    property_code: "mode"
                    value: "auto"
          
          - type: entities
            entities:
              - entity: input_number.tuya_temp_set
              - entity: input_select.tuya_windspeed
              - entity: input_boolean.tuya_freshair_filter
```

### 3) Sensor-Heavy Dashboard

```yaml
views:
  - title: Sensoren
    cards:
      - type: entities
        title: "Temperaturen"
        entities:
          - entity: sensor.tuya_temp_current
            name: "Aktuell"
          - entity: input_number.tuya_temp_set
            name: "Sollwert"
          - entity: sensor.tuya_humidity_current
            name: "Luftfeuchte"
      
      - type: entities
        title: "Luftqualität"
        entities:
          - entity: sensor.tuya_pm25
            name: "PM2.5"
          - entity: sensor.tuya_airquality
            name: "Air Quality"
      
      - type: entities
        title: "Filter"
        entities:
          - entity: input_boolean.tuya_dirty_filter
            name: "Filter verschmutzt"
          - entity: input_boolean.tuya_freshair_filter
            name: "Frischluftfilter"
```

---

## Script-Beispiele

### Heating Script

```yaml
script:
  tuya_set_heating:
    sequence:
      - service: pyscript.tuya_set_property
        data:
          property_code: "mode"
          value: "hot"
      - service: pyscript.tuya_set_property
        data:
          property_code: "temp_set"
          value: "{{ (target_temp | int * 10) }}"
      - service: notify.mobile_app_user
        data:
          message: "Heizen auf {{ target_temp }}°C"
```

Aufruf in Automation:

```yaml
action:
  - service: script.tuya_set_heating
    data:
      target_temp: 22
```

---

## Häufige Aufgaben

### 1️⃣ Wert sichtbar in Dashboard machen

```yaml
# In helpers.yaml
input_number:
  tuya_temp_display:
    name: "Temperatur"
    min: 0
    max: 50
    unit_of_measurement: "°C"

# In automation.yaml
- alias: "Update Temp Display"
  trigger:
    platform: time_pattern
    minutes: 1
  action:
    - service: input_number.set_value
      target:
        entity_id: input_number.tuya_temp_display
      data:
        value: "{{ ((states('sensor.tuya_temp_current') | int(0)) / 10) | round(1) }}"
```

### 2️⃣ Buttons für schnelle Kontrolle

```yaml
- type: custom:button-card
  name: "22°C"
  tap_action:
    action: call-service
    service: pyscript.tuya_set_property
    data:
      property_code: "temp_set"
      value: 220
```

### 3️⃣ Bedingte Sichtbarkeit

```yaml
- entity: input_boolean.tuya_power
  visible: "{{ is_state('input_select.tuya_mode', 'heat') }}"
```

### 4️⃣ History Graph

```yaml
- type: history-graph
  title: "Temperatur Verlauf"
  entities:
    - entity: sensor.tuya_temp_current
  hours_to_show: 24
```

---

## Mobil-Benachrichtigungen

```yaml
automation:
  - alias: "Mobile Alert: High Temperature"
    trigger:
      platform: numeric_state
      entity_id: sensor.tuya_temp_current
      above: 280  # > 28°C
    action:
      - service: notify.mobile_app_user_iphone
        data:
          message: "Temperatur zu hoch: {{ states('sensor.tuya_temp_current') }}"
          title: "⚠️ Alarm"
          data:
            actions:
              - action: COOL_DOWN
                title: "Kühlen"
              - action: IGNORE
                title: "Ignorieren"
      
      - wait_for_trigger:
          platform: event
          event_type: mobile_app_notification_action
      
      - choose:
          - conditions: "{{ trigger.event.data.action == 'COOL_DOWN' }}"
            sequence:
              - service: pyscript.tuya_set_property
                data:
                  property_code: "mode"
                  value: "cool"
```

---

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| Services nicht sichtbar | HA neu starten, PyScript reload |
| Werte aktualisieren nicht | Update-Interval erhöhen, Logs checken |
| Credential Fehler | API Keys überprüfen, Token regenerieren |
| Timeout-Fehler | Netzwerk checken, Tuya Cloud erreichbar? |

Fragen? Schau dir die PyScript-Logs an:
`Configuration → System → Logs → PyScript`
