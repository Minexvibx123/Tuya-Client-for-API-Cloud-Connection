#!/bin/bash
# Tuya Client REST API - Installation Script from GitHub
# Automatisches Download & Installation auf Raspberry Pi / Linux
# 
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection/main/install_rest_api.sh | bash

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🏠 Tuya Client REST API - Installation Script            ║"
echo "║  GitHub: Minexvibx123/Tuya-Client-for-API-Cloud-Connection║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# 1. ÜBERPRÜFUNG: Python installiert?
# ============================================================

echo "1️⃣  Prüfe Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nicht gefunden. Installiere..."
    apt-get update
    apt-get install -y python3 python3-pip
else
    echo "✓ Python3 gefunden: $(python3 --version)"
fi

# ============================================================
# 2. ÜBERPRÜFUNG: git installiert?
# ============================================================

echo ""
echo "2️⃣  Prüfe git..."
if ! command -v git &> /dev/null; then
    echo "ℹ️  git nicht gefunden. Installiere..."
    apt-get update
    apt-get install -y git
else
    echo "✓ git gefunden: $(git --version)"
fi

# ============================================================
# 3. DOWNLOAD: Projekt von GitHub
# ============================================================

echo ""
echo "3️⃣  Lade Projekt von GitHub herunter..."

INSTALL_DIR="/root/tuya_client"

if [ -d "$INSTALL_DIR" ]; then
    echo "ℹ️  Verzeichnis $INSTALL_DIR existiert bereits."
    echo "   Wähle eine Option:"
    echo "   1) Überschreiben (git pull)"
    echo "   2) Beende Installation"
    read -p "Deine Wahl [1/2]: " choice
    
    if [ "$choice" = "1" ]; then
        cd "$INSTALL_DIR"
        git pull origin main
        echo "✓ Projekt aktualisiert"
    else
        echo "❌ Installation abgebrochen"
        exit 0
    fi
else
    echo "Klone Repository..."
    git clone https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    echo "✓ Projekt heruntergeladen nach: $INSTALL_DIR"
fi

# ============================================================
# 4. DEPENDENCIES: Installiere Requirements
# ============================================================

echo ""
echo "4️⃣  Installiere Python Dependencies..."

if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo "✓ Requirements installiert"
else
    echo "❌ requirements.txt nicht gefunden!"
    exit 1
fi

# Extra Dependencies für REST API
echo "   Installiere Flask Dependencies..."
pip install -q flask flask-cors

# ============================================================
# 5. CONFIG: config.yaml überprüfen
# ============================================================

echo ""
echo "5️⃣  Überprüfe Konfiguration..."

if [ ! -f "config.yaml" ]; then
    echo "❌ config.yaml nicht gefunden!"
    echo ""
    echo "Erstelle config.yaml mit deinen Credentials:"
    echo "---"
    
    read -p "Tuya Access ID: " ACCESS_ID
    read -p "Tuya Access Key: " ACCESS_KEY
    read -p "Tuya Device ID: " DEVICE_ID
    read -p "Tuya Region [eu/us/cn]: " REGION
    REGION=${REGION:-eu}
    
    cat > config.yaml <<EOF
tuya_api:
  access_id: "$ACCESS_ID"
  access_key: "$ACCESS_KEY"
  device_id: "$DEVICE_ID"
  region: "$REGION"
EOF
    
    echo "✓ config.yaml erstellt"
else
    echo "✓ config.yaml existiert"
fi

# ============================================================
# 6. SERVICE: Erstelle Systemd Service (Optional)
# ============================================================

echo ""
echo "6️⃣  Richte Systemd Service ein (optional)..."
echo ""
read -p "Soll die API als Service starten (Autostart)? [j/n]: " install_service

if [ "$install_service" = "j" ] || [ "$install_service" = "y" ]; then
    SERVICE_FILE="/etc/systemd/system/tuya-api.service"
    
    cat > /tmp/tuya-api.service <<EOF
[Unit]
Description=Tuya Client REST API
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/src/tuya_homeassistant_api.py --port 5000
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    cp /tmp/tuya-api.service "$SERVICE_FILE"
    systemctl daemon-reload
    systemctl enable tuya-api
    systemctl start tuya-api
    
    echo "✓ Service erstellt und aktiviert"
    echo "  Starten: systemctl start tuya-api"
    echo "  Status: systemctl status tuya-api"
    echo "  Logs: journalctl -u tuya-api -f"
else
    echo "ℹ️  Service nicht installiert (manueller Start erforderlich)"
fi

# ============================================================
# 7. VERIFIZIERUNG
# ============================================================

echo ""
echo "7️⃣  Verifiziere Installation..."

sleep 2

if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✓ REST API läuft auf http://localhost:5000"
    curl -s http://localhost:5000/health | python3 -m json.tool
else
    echo "⚠️  API läuft noch nicht. Starten Sie manuell:"
    echo "   cd $INSTALL_DIR"
    echo "   python3 src/tuya_homeassistant_api.py --port 5000"
fi

# ============================================================
# FERTIG
# ============================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Installation abgeschlossen!                           ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  Installation Verzeichnis: $INSTALL_DIR"
echo "║  Dokumentation: $INSTALL_DIR/docs/HOMEASSISTANT_QUICKSTART.md"
echo "║  Config: $INSTALL_DIR/config.yaml"
echo "║"
echo "║  Nächste Schritte:"
echo "║  1. config.yaml überprüfen: nano $INSTALL_DIR/config.yaml"
echo "║  2. API testen: curl http://localhost:5000/health"
echo "║  3. In Home Assistant konfigurieren (REST Commands)"
echo "║"
echo "║  Support: https://github.com/Minexvibx123/Tuya-Client-for-API-Cloud-Connection"
echo "╚════════════════════════════════════════════════════════════╝"
