#!/usr/bin/env python3
"""
TUYA CLOUD CLIENT - MODERNES GUI
Moderne Benutzeroberfläche zur Steuerung von Tuya Smart Home Geräten
"""

import sys
import json
import time
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QSpinBox, QSlider, QTabWidget,
    QTableWidget, QTableWidgetItem, QStatusBar, QDialog, QMessageBox,
    QGridLayout, QGroupBox, QFrame, QProgressBar, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap
import yaml
from client import TuyaCloudClient


class DeviceWorker(QThread):
    """Worker Thread für Device-Operationen ohne GUI-Blockierung"""
    
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(dict)
    
    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args
        self.client = TuyaCloudClient()
    
    def run(self):
        try:
            if self.operation == "get_token":
                token = self.client.get_token()
                self.result.emit({"token": token})
            
            elif self.operation == "get_status":
                device_id, token = self.args
                status = self.client.get_device_status(device_id, token)
                self.result.emit({"status": status})
            
            elif self.operation == "get_properties":
                device_id, token = self.args
                props = self.client.get_device_properties(device_id, token)
                self.result.emit({"properties": props})
            
            elif self.operation == "set_property":
                device_id, token, code, value = self.args
                result = self.client.set_device_property(device_id, token, code, value)
                self.result.emit({"success": result, "code": code, "value": value})
            
            self.finished.emit()
        
        except Exception as e:
            self.error.emit(str(e))


class TuyaGUI(QMainWindow):
    """Hauptfenster mit modernem Design"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tuya Smart Home Control")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_dark_stylesheet())
        
        # Config laden
        self.config = self.load_config()
        self.device_id = self.config['devices'][0]['device_id']
        self.device_name = self.config['devices'][0]['name']
        
        # Client
        self.client = TuyaCloudClient()
        self.token = None
        self.properties = {}
        
        # Worker
        self.worker = None
        
        # Initialisiere UI
        self.init_ui()
        
        # Starte erste Initialisierung
        self.on_startup()
    
    def load_config(self) -> dict:
        """Lädt config.yaml"""
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    
    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_status_tab(), "📊 Status")
        tabs.addTab(self.create_control_tab(), "🎛️ Steuerung")
        tabs.addTab(self.create_properties_tab(), "📋 Properties")
        tabs.addTab(self.create_config_tab(), "⚙️ Konfiguration")
        
        main_layout.addWidget(tabs)
        
        # Status Bar
        self.statusBar().showMessage("Verbindung wird hergestellt...")
    
    def create_header(self) -> QWidget:
        """Erstellt Header mit Geräteinformationen"""
        header = QFrame()
        header.setStyleSheet("background-color: #1e1e1e; border-radius: 8px; padding: 15px;")
        
        layout = QHBoxLayout()
        
        # Gerätename
        device_label = QLabel(f"🏠 {self.device_name}")
        device_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        device_label.setStyleSheet("color: #00ff00;")
        layout.addWidget(device_label)
        
        # Status Indicator
        self.status_indicator = QLabel("🔴 Offline")
        self.status_indicator.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_indicator.setStyleSheet("color: #ff4444;")
        layout.addWidget(self.status_indicator)
        
        # IP Address
        self.ip_label = QLabel("IP: -")
        self.ip_label.setStyleSheet("color: #aaaaaa;")
        layout.addWidget(self.ip_label)
        
        layout.addStretch()
        
        # Refresh Button
        refresh_btn = QPushButton("🔄 Aktualisieren")
        refresh_btn.setStyleSheet(self.get_button_style("#0066cc"))
        refresh_btn.clicked.connect(self.refresh_properties)
        layout.addWidget(refresh_btn)
        
        header.setLayout(layout)
        return header
    
    def create_status_tab(self) -> QWidget:
        """Status Tab mit Echtzeit-Daten"""
        widget = QWidget()
        layout = QGridLayout()
        
        # Power Status
        power_group = QGroupBox("⚡ Power")
        power_layout = QVBoxLayout()
        self.power_label = QLabel("Status: -")
        self.power_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        power_layout.addWidget(self.power_label)
        power_group.setLayout(power_layout)
        layout.addWidget(power_group, 0, 0)
        
        # Temperature Status
        temp_group = QGroupBox("🌡️ Temperatur")
        temp_layout = QGridLayout()
        self.temp_current = QLabel("Aktuell: - °C")
        self.temp_current.setFont(QFont("Arial", 12))
        self.temp_setpoint = QLabel("Sollwert: - °C")
        self.temp_setpoint.setFont(QFont("Arial", 12))
        temp_layout.addWidget(self.temp_current, 0, 0)
        temp_layout.addWidget(self.temp_setpoint, 1, 0)
        temp_group.setLayout(temp_layout)
        layout.addWidget(temp_group, 0, 1)
        
        # Mode Status
        mode_group = QGroupBox("🔄 Betriebsmodus")
        mode_layout = QVBoxLayout()
        self.mode_label = QLabel("Modus: -")
        self.mode_label.setFont(QFont("Arial", 12))
        mode_layout.addWidget(self.mode_label)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group, 1, 0)
        
        # Windspeed Status
        wind_group = QGroupBox("💨 Windgeschwindigkeit")
        wind_layout = QVBoxLayout()
        self.wind_label = QLabel("Windspeed: -")
        self.wind_label.setFont(QFont("Arial", 12))
        wind_layout.addWidget(self.wind_label)
        wind_group.setLayout(wind_layout)
        layout.addWidget(wind_group, 1, 1)
        
        # Humidity
        humid_group = QGroupBox("💧 Luftfeuchte")
        humid_layout = QVBoxLayout()
        self.humid_label = QLabel("Feuchte: - %")
        self.humid_label.setFont(QFont("Arial", 12))
        humid_layout.addWidget(self.humid_label)
        humid_group.setLayout(humid_layout)
        layout.addWidget(humid_group, 2, 0)
        
        # Air Quality
        air_group = QGroupBox("🌬️ Luftqualität")
        air_layout = QVBoxLayout()
        self.air_label = QLabel("Qualität: -")
        self.air_label.setFont(QFont("Arial", 12))
        air_layout.addWidget(self.air_label)
        air_group.setLayout(air_layout)
        layout.addWidget(air_group, 2, 1)
        
        layout.setRowStretch(3, 1)
        widget.setLayout(layout)
        return widget
    
    def create_control_tab(self) -> QWidget:
        """Steuerungs Tab mit Kontrollelementen"""
        widget = QWidget()
        layout = QGridLayout()
        
        # Power Control
        power_group = QGroupBox("⚡ Power")
        power_layout = QHBoxLayout()
        self.power_on_btn = QPushButton("An")
        self.power_on_btn.setStyleSheet(self.get_button_style("#00cc00"))
        self.power_on_btn.clicked.connect(lambda: self.set_property("Power", True))
        self.power_off_btn = QPushButton("Aus")
        self.power_off_btn.setStyleSheet(self.get_button_style("#cc0000"))
        self.power_off_btn.clicked.connect(lambda: self.set_property("Power", False))
        power_layout.addWidget(self.power_on_btn)
        power_layout.addWidget(self.power_off_btn)
        power_group.setLayout(power_layout)
        layout.addWidget(power_group, 0, 0, 1, 2)
        
        # Mode Selection
        mode_group = QGroupBox("🔄 Betriebsmodus")
        mode_layout = QHBoxLayout()
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["hot", "cold", "wind", "dry"])
        self.mode_combo.currentTextChanged.connect(
            lambda text: self._on_mode_changed(text)
        )
        mode_layout.addWidget(self.mode_combo)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group, 1, 0, 1, 2)
        
        # Temperature Control
        temp_group = QGroupBox("🌡️ Solltemperatur")
        temp_layout = QHBoxLayout()
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setMinimum(160)  # 16°C
        self.temp_slider.setMaximum(300)  # 30°C
        self.temp_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.temp_slider.setTickInterval(10)
        self.temp_slider.sliderMoved.connect(self.on_temp_slider_moved)
        self.temp_spin = QSpinBox()
        self.temp_spin.setMinimum(16)
        self.temp_spin.setMaximum(30)
        self.temp_spin.setSuffix("°C")
        self.temp_spin.valueChanged.connect(self.on_temp_spin_changed)
        self.temp_display = QLabel("- °C")
        self.temp_display.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.temp_display.setStyleSheet("color: #00ff00;")
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_spin)
        temp_layout.addWidget(self.temp_display)
        temp_group.setLayout(temp_layout)
        layout.addWidget(temp_group, 2, 0, 1, 2)
        
        # Windspeed Control
        wind_group = QGroupBox("💨 Windgeschwindigkeit")
        wind_layout = QHBoxLayout()
        self.wind_combo = QComboBox()
        self.wind_combo.addItems(["auto", "1", "2", "3"])
        self.wind_combo.currentTextChanged.connect(
            lambda: self.set_property("windspeed", self.wind_combo.currentText())
        )
        wind_layout.addWidget(self.wind_combo)
        wind_group.setLayout(wind_layout)
        layout.addWidget(wind_group, 3, 0, 1, 2)
        
        layout.setRowStretch(4, 1)
        widget.setLayout(layout)
        return widget
    
    def create_properties_tab(self) -> QWidget:
        """Properties Tab mit Tabelle aller Properties - interaktiv änderbar"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Anleitung
        info_label = QLabel("💡 Klicke auf eine Property um den Wert zu ändern")
        info_label.setStyleSheet("color: #aaaaaa; padding: 10px;")
        layout.addWidget(info_label)
        
        self.properties_table = QTableWidget()
        self.properties_table.setColumnCount(5)
        self.properties_table.setHorizontalHeaderLabels(["Code", "Typ", "Aktuell", "✏️ Ändern", "DP_ID"])
        self.properties_table.horizontalHeader().setStretchLastSection(False)
        self.properties_table.setColumnWidth(0, 140)
        self.properties_table.setColumnWidth(1, 70)
        self.properties_table.setColumnWidth(2, 100)
        self.properties_table.setColumnWidth(3, 200)
        self.properties_table.setColumnWidth(4, 100)
        
        layout.addWidget(self.properties_table)
        widget.setLayout(layout)
        return widget
    
    def on_startup(self):
        """Starte Initialisierung"""
        self.worker = DeviceWorker("get_token")
        self.worker.result.connect(self.on_token_received)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_token_received(self, data):
        """Token empfangen"""
        self.token = data['token']
        if self.token:
            self.statusBar().showMessage("✓ Token erhalten")
            self.refresh_properties()
        else:
            self.statusBar().showMessage("✗ Token-Fehler")
    
    def refresh_properties(self):
        """Aktualisiere alle Properties"""
        if not self.token:
            return
        
        self.worker = DeviceWorker("get_properties", self.device_id, self.token)
        self.worker.result.connect(self.on_properties_received)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_properties_received(self, data):
        """Properties empfangen"""
        self.properties = data['properties']
        self.update_ui_from_properties()
        
        # Auch Status abrufen
        self.worker = DeviceWorker("get_status", self.device_id, self.token)
        self.worker.result.connect(self.on_status_received)
        self.worker.start()
    
    def on_status_received(self, data):
        """Status empfangen"""
        status = data['status']
        
        # Update Header
        is_online = status.get('is_online', False)
        self.status_indicator.setText("🟢 Online" if is_online else "🔴 Offline")
        self.status_indicator.setStyleSheet("color: #00ff00;" if is_online else "color: #ff4444;")
        self.ip_label.setText(f"IP: {status.get('ip', '-')}")
    
    def _on_mode_changed(self, text: str):
        """Mode kombobox geändert"""
        # Nur setzen wenn Text nicht leer ist (während Initialisierung)
        if text and not self.mode_combo.signalsBlocked():
            self.set_property("mode", text)
    
    def update_ui_from_properties(self):
        """Update UI mit den aktuellen Properties"""
        if not self.properties:
            return
        
        # Power
        power_val = self.properties.get('Power', {}).get('value', False)
        self.power_label.setText(f"Status: {'✓ An' if power_val else '✗ Aus'}")
        self.power_label.setStyleSheet("color: #00ff00;" if power_val else "color: #ff4444;")
        
        # Temperature
        temp_cur = self.properties.get('temp_current', {}).get('value', '-')
        temp_set = self.properties.get('temp_set', {}).get('value', '-')
        if temp_cur != '-':
            self.temp_current.setText(f"Aktuell: {temp_cur}°C")
        if temp_set != '-':
            temp_celsius = temp_set / 10
            self.temp_setpoint.setText(f"Sollwert: {temp_celsius}°C")
            self.temp_slider.blockSignals(True)
            self.temp_spin.blockSignals(True)
            self.temp_slider.setValue(temp_set)
            self.temp_spin.setValue(int(temp_celsius))
            self.temp_display.setText(f"{temp_celsius}°C")
            self.temp_slider.blockSignals(False)
            self.temp_spin.blockSignals(False)
        
        # Mode
        mode = self.properties.get('mode', {}).get('value', '-')
        self.mode_label.setText(f"Modus: {mode}")
        self.mode_combo.blockSignals(True)
        self.mode_combo.setCurrentText(mode)
        self.mode_combo.blockSignals(False)
        
        # Windspeed
        wind = self.properties.get('windspeed', {}).get('value', '-')
        self.wind_label.setText(f"Windspeed: {wind}")
        self.wind_combo.blockSignals(True)
        if wind in ["auto", "1", "2", "3"]:
            self.wind_combo.setCurrentText(wind)
        self.wind_combo.blockSignals(False)
        
        # Humidity
        humid = self.properties.get('humidity_current', {}).get('value', '-')
        self.humid_label.setText(f"Feuchte: {humid}%")
        
        # Air Quality
        air = self.properties.get('airquality', {}).get('value', '-')
        self.air_label.setText(f"Qualität: {air}")
        
        # Properties Table
        self.update_properties_table()
    
    def update_properties_table(self):
        """Update Properties Tabelle mit interaktiven Edit-Elementen"""
        self.properties_table.setRowCount(len(self.properties))
        
        for row, (code, info) in enumerate(sorted(self.properties.items())):
            # Code (editable)
            code_item = QTableWidgetItem(code)
            self.properties_table.setItem(row, 0, code_item)
            
            # Type
            prop_type = info.get('type', '-')
            self.properties_table.setItem(row, 1, QTableWidgetItem(str(prop_type)))
            
            # Aktueller Wert
            current_value = info.get('value', '-')
            self.properties_table.setItem(row, 2, QTableWidgetItem(str(current_value)))
            
            # Edit Widget (interaktiv)
            edit_widget = QWidget()
            edit_layout = QHBoxLayout()
            edit_layout.setContentsMargins(0, 0, 0, 0)
            
            # Only allow editing for specific property types
            editable_types = ['bool', 'value', 'enum', 'string']
            
            if prop_type in editable_types:
                if prop_type == 'bool':
                    # Toggle Switch für Boolean
                    toggle_btn = QPushButton("✓" if current_value else "✗")
                    toggle_btn.setStyleSheet(self.get_button_style("#0066cc"))
                    toggle_btn.setMaximumWidth(50)
                    toggle_btn.setMaximumHeight(30)
                    toggle_btn.clicked.connect(
                        lambda checked, c=code: self.set_property(c, not self.properties[c]['value'])
                    )
                    edit_layout.addWidget(toggle_btn)
                
                else:
                    # Textfield für alle anderen Typen
                    text_input = QLineEdit(str(current_value))
                    text_input.setMaximumHeight(30)
                    text_input.setMaximumWidth(150)
                    text_input.setStyleSheet("""
                        QLineEdit {
                            background-color: #1e1e1e;
                            color: #ffffff;
                            border: 1px solid #0066cc;
                            border-radius: 3px;
                            padding: 3px;
                            font-size: 12px;
                        }
                    """)
                    text_input.returnPressed.connect(
                        lambda c=code, t=text_input, pt=prop_type: self.set_property(c, self.parse_input_value(t.text(), pt))
                    )
                    edit_layout.addWidget(text_input)
            else:
                # Label für Read-Only
                label = QLabel("(Read-Only)")
                label.setStyleSheet("color: #888888;")
                edit_layout.addWidget(label)
            
            edit_layout.addStretch()
            edit_widget.setLayout(edit_layout)
            self.properties_table.setCellWidget(row, 3, edit_widget)
            
            # DP_ID
            self.properties_table.setItem(row, 4, QTableWidgetItem(str(info.get('dp_id', '-'))))
    
    def parse_input_value(self, text: str, prop_type: str = None) -> Any:
        """Konvertiert Text-Input zu passendem Datentyp basierend auf Property Type"""
        text = text.strip()
        
        # Wenn Property Type bekannt ist, verwende ihn
        if prop_type == 'string':
            return text  # Strings bleiben Strings!
        
        # Für boolean type
        if prop_type == 'bool':
            text_lower = text.lower()
            if text_lower in ['true', 'on', 'yes', 'an']:
                return True
            if text_lower in ['false', 'off', 'no', 'aus']:
                return False
            # Auch 1/0 akzeptieren
            try:
                return bool(int(text))
            except (ValueError, TypeError):
                return False
        
        # Für numerische Typen
        if prop_type == 'value':
            try:
                if '.' in text:
                    return float(text)
                return int(text)
            except (ValueError, TypeError):
                return 0
        
        # Fallback: Versuche zu raten
        text_lower = text.lower()
        
        # Boolean-ähnliche Werte
        if text_lower in ['true', 'on', 'yes', 'an']:
            return True
        if text_lower in ['false', 'off', 'no', 'aus']:
            return False
        
        # Zahlen
        try:
            if '.' in text:
                return float(text)
            return int(text)
        except ValueError:
            pass
        
        # Default: als String zurückgeben
        return text
    
    def set_property(self, code: str, value: Any):
        """Setzt eine Property"""
        if not self.token:
            self.show_error("Kein Token vorhanden")
            return
        
        # Convert value to appropriate type based on property type
        if code in self.properties:
            prop_type = self.properties[code].get('type')
            
            # For boolean properties (true bool type)
            if prop_type == 'bool':
                value = bool(value)
            # For numeric values (including boolcode which is a number)
            elif prop_type == 'value':
                try:
                    value = int(value) if isinstance(value, (int, float, bool)) else int(float(value))
                except (ValueError, TypeError):
                    value = 0
        
        self.statusBar().showMessage(f"Setze {code} = {value}...")
        
        self.worker = DeviceWorker("set_property", self.device_id, self.token, code, value)
        self.worker.result.connect(self.on_property_set)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_property_set(self, data):
        """Property gesetzt"""
        if data.get('success'):
            self.statusBar().showMessage(f"✓ {data['code']} gesetzt")
            time.sleep(0.5)
            self.refresh_properties()
        else:
            self.statusBar().showMessage(f"✗ Fehler beim Setzen von {data['code']}")
    
    def on_temp_slider_moved(self, value):
        """Temperature Slider bewegt"""
        celsius = value / 10
        self.temp_spin.blockSignals(True)
        self.temp_spin.setValue(int(celsius))
        self.temp_spin.blockSignals(False)
        self.temp_display.setText(f"{celsius}°C")
        self.set_property("temp_set", value)
    
    def on_temp_spin_changed(self, value):
        """Temperature Spin Box geändert"""
        temp_value = value * 10
        self.temp_slider.blockSignals(True)
        self.temp_slider.setValue(temp_value)
        self.temp_slider.blockSignals(False)
        self.temp_display.setText(f"{value}°C")
    
    
    def on_error(self, error_msg):
        """Fehler anzeigen"""
        self.show_error(f"Fehler: {error_msg}")
        self.statusBar().showMessage(f"✗ Fehler: {error_msg}")
    
    def show_error(self, message: str):
        """Zeigt Error Dialog"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Fehler")
        msg_box.setText(message)
        msg_box.setStyleSheet(self.get_dark_stylesheet())
        msg_box.exec()
    
    def create_config_tab(self) -> QWidget:
        """Erstellt Configuration Tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Überschrift
        title = QLabel("Konfiguration")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff00; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # API Konfiguration
        api_group = QGroupBox("API Konfiguration")
        api_layout = QGridLayout()
        
        # Access ID
        api_layout.addWidget(QLabel("Access ID:"), 0, 0)
        access_id_field = QLineEdit()
        access_id_field.setText(self.config.get('cloud', {}).get('access_id', ''))
        access_id_field.setReadOnly(True)
        api_layout.addWidget(access_id_field, 0, 1)
        
        # Access Key
        api_layout.addWidget(QLabel("Access Key:"), 1, 0)
        access_key_field = QLineEdit()
        access_key_field.setText("*" * 20)  # Versteckt das echte Key
        access_key_field.setReadOnly(True)
        api_layout.addWidget(access_key_field, 1, 1)
        
        # Region
        api_layout.addWidget(QLabel("Region:"), 2, 0)
        region_field = QLineEdit()
        region_field.setText(self.config.get('cloud', {}).get('region', ''))
        region_field.setReadOnly(True)
        api_layout.addWidget(region_field, 2, 1)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Geräte Konfiguration
        device_group = QGroupBox("Geräte")
        device_layout = QGridLayout()
        
        devices = self.config.get('devices', [])
        for idx, device in enumerate(devices):
            device_layout.addWidget(QLabel(f"Gerät {idx+1}:"), idx, 0)
            device_info = QLineEdit()
            device_info.setText(f"{device.get('name', 'N/A')} ({device.get('device_id', 'N/A')[:8]}...)")
            device_info.setReadOnly(True)
            device_layout.addWidget(device_info, idx, 1)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Debug Einstellungen
        debug_group = QGroupBox("Debug Einstellungen")
        debug_layout = QGridLayout()
        
        debug_layout.addWidget(QLabel("Debug:"), 0, 0)
        debug_field = QLineEdit()
        debug_field.setText(str(self.config.get('debug', False)))
        debug_field.setReadOnly(True)
        debug_layout.addWidget(debug_field, 0, 1)
        
        debug_layout.addWidget(QLabel("Log Level:"), 1, 0)
        loglevel_field = QLineEdit()
        loglevel_field.setText(self.config.get('log_level', 'INFO'))
        loglevel_field.setReadOnly(True)
        debug_layout.addWidget(loglevel_field, 1, 1)
        
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)
        
        # Info Text
        info_text = QLabel(
            "⚠️ Konfiguration ist schreibgeschützt.\n"
            "Bearbeite config.yaml um Einstellungen zu ändern."
        )
        info_text.setStyleSheet("color: #ffaa00; margin-top: 15px;")
        layout.addWidget(info_text)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    @staticmethod
    def get_dark_stylesheet() -> str:
        """Modernes dunkles Design"""
        return """
        QMainWindow, QWidget {
            background-color: #0d0d0d;
            color: #ffffff;
            font-family: 'Segoe UI', Arial;
        }
        
        QTabWidget::pane {
            border: 1px solid #333333;
        }
        
        QTabBar::tab {
            background-color: #1a1a1a;
            color: #aaaaaa;
            padding: 8px 20px;
            border: 1px solid #333333;
            border-radius: 4px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #0066cc;
            color: #ffffff;
        }
        
        QGroupBox {
            color: #ffffff;
            border: 1px solid #333333;
            border-radius: 6px;
            padding: 10px;
            margin-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
        }
        
        QPushButton {
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: bold;
            border: none;
            min-height: 35px;
        }
        
        QPushButton:hover {
            opacity: 0.8;
        }
        
        QPushButton:pressed {
            opacity: 0.6;
        }
        
        QComboBox {
            background-color: #1a1a1a;
            color: #ffffff;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 5px;
            min-height: 30px;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QSpinBox {
            background-color: #1a1a1a;
            color: #ffffff;
            border: 1px solid #333333;
            border-radius: 4px;
            padding: 5px;
            min-height: 30px;
        }
        
        QSlider::groove:horizontal {
            background-color: #1a1a1a;
            height: 6px;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background-color: #0066cc;
            width: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        
        QTableWidget {
            background-color: #1a1a1a;
            gridline-color: #333333;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QHeaderView::section {
            background-color: #0066cc;
            color: #ffffff;
            padding: 5px;
            border: none;
        }
        
        QStatusBar {
            background-color: #1a1a1a;
            color: #aaaaaa;
            border-top: 1px solid #333333;
        }
        
        QLabel {
            color: #ffffff;
        }
        """
    
    @staticmethod
    def get_button_style(color: str) -> str:
        """Erstellt Button Style mit Farbe"""
        return f"""
        QPushButton {{
            background-color: {color};
            color: #ffffff;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
            border: none;
            min-height: 35px;
        }}
        QPushButton:hover {{
            opacity: 0.8;
        }}
        QPushButton:pressed {{
            opacity: 0.6;
        }}
        """


def main():
    app = QApplication(sys.argv)
    gui = TuyaGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
