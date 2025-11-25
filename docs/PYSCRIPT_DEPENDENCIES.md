# PyScript Dependencies - Detaillierte Anleitung

## 📦 Was sind Dependencies?

Dependencies sind Python-Bibliotheken, die dein Code braucht um zu funktionieren.

**Für Tuya Client brauchen wir:**
- `requests` - HTTP-Anfragen zu Tuya API
- `yaml` - YAML-Konfigurationen lesen
- `hmac`, `hashlib`, `json`, `time`, `logging` - bereits in Python enthalten

---

## 🚀 Automatische Installation (Empfohlen)

### Schritt 1: HACS installieren

```
Home Assistant → Einstellungen → Geräte & Dienste
  → "+ Neue Integration erstellen"
  → Suche: "HACS"
  → "INSTALL"
```

Oder direkt: https://www.hacs.xyz/

### Schritt 2: PyScript via HACS installieren

```
Home Assistant → HACS (oben rechts)
  → "Automation" (linkes Menü)
  → "Erkunden & Herunterladen Repositories"
  → Suche: "pyscript"
  → "pyscript by balloob"
  → "INSTALL"
  → Restart Home Assistant
```

### Schritt 3: configuration.yaml aktualisieren

```yaml
# /config/configuration.yaml

pyscript:
  allow_all_imports: true    # ← WICHTIG!
  file_reloader: true
```

### Schritt 4: Home Assistant neu starten

```
Einstellungen → System → "Home Assistant neu starten"
```

**Fertig!** PyScript lädt jetzt automatisch alle Dependencies herunter.

---

## 🔧 Manuelle Installation

Wenn automatisches Laden nicht funktioniert:

### Option A: SSH Terminal

**Voraussetzung:** SSH Add-on installiert

```
Einstellungen → Zusatzprogramme
  → Alle Add-ons anzeigen
  → "Terminal & SSH"
  → "INSTALL"
```

**Dependencies installieren:**

```bash
# SSH verbinden (192.168.1.100 = deine HA IP)
ssh root@192.168.1.100

# Dependencies installieren
pip install requests pyyaml

# Überprüfen
python3 -c "import requests, yaml; print('✓ OK')"

# Home Assistant neu starten
systemctl restart homeassistant
```

### Option B: Home Assistant Container/Docker

```bash
# Von deinem Host-System
docker exec homeassistant pip install requests pyyaml

# Überprüfen
docker exec homeassistant python3 -c "import requests, yaml; print('✓ OK')"

# Home Assistant neu starten
docker restart homeassistant
```

### Option C: Home Assistant OS (Supervised)

```bash
# SSH als root verbinden
ssh root@192.168.1.100

# In den Home Assistant Container gehen
docker exec -it homeassistant bash

# Dependencies installieren
pip install requests pyyaml

# Beenden
exit

# Home Assistant neu starten
```

---

## ✅ Überprüfung

### 1. Developer Tools Methode

```
Home Assistant → Developer Tools → Services
Suche: "pyscript"
```

Wenn Services wie `pyscript.tuya_update_all` sichtbar sind → ✓ OK

### 2. Logs Methode

```
Einstellungen → System → Logs
Suche: "pyscript"
```

Darf kein Import-Error zeigen:
```
❌ Fehler: ImportError: No module named 'requests'
✅ Gut: Successfully imported all modules
```

### 3. Python Shell Methode

```
Developer Tools → Template
Teste:
{{ range(1) | list }}
```

Dann teste direkt in PyScript (`/config/pyscript/test.py`):
```python
import requests
import yaml
log.info("✓ Alle Dependencies OK!")
```

### 4. PyScript File Test

Erstelle `/config/pyscript/test_deps.py`:

```python
"""Test Dependencies"""
import logging
_LOGGER = logging.getLogger(__name__)

try:
    import requests
    _LOGGER.info("✓ requests: OK")
except ImportError:
    _LOGGER.error("✗ requests: FEHLER")

try:
    import yaml
    _LOGGER.info("✓ yaml: OK")
except ImportError:
    _LOGGER.error("✗ yaml: FEHLER")

try:
    import hmac
    import hashlib
    import json
    import time
    _LOGGER.info("✓ Standard libs: OK")
except ImportError:
    _LOGGER.error("✗ Standard libs: FEHLER")
```

Home Assistant neu starten und Logs checken.

---

## 🐛 Häufige Fehler & Lösungen

### Fehler 1: "ModuleNotFoundError: No module named 'requests'"

**Ursache:** `allow_all_imports` nicht gesetzt oder false

**Lösung:**
```yaml
# configuration.yaml
pyscript:
  allow_all_imports: true    # ← Setzen auf true!
```
Dann neu starten.

---

### Fehler 2: "No module named 'yaml'"

**Ursache:** PyYAML nicht installiert

**Lösung:**
```bash
# SSH terminal
pip install pyyaml    # ← PyYAML nicht yaml!
```

---

### Fehler 3: "Permission denied"

**Ursache:** Keine Admin-Rechte

**Lösung:**
```bash
# Mit sudo versuchen
sudo pip install requests pyyaml

# Oder als homeassistant user:
sudo -u homeassistant pip install requests pyyaml
```

---

### Fehler 4: "pip: command not found"

**Ursache:** pip nicht in PATH oder Python nicht installiert

**Lösung:**
```bash
# Python3 pip verwenden
python3 -m pip install requests pyyaml

# Oder vollständiger Pfad:
/usr/bin/python3 -m pip install requests pyyaml
```

---

### Fehler 5: "Requirements already satisfied"

**Status:** Alles OK! Dependencies sind bereits installiert.

```
✓ Successfully installed requests-2.28.0 pyyaml-6.0
```

---

## 📋 Checkliste

### Automatische Installation
- [ ] HACS installiert
- [ ] PyScript via HACS installiert
- [ ] `allow_all_imports: true` in configuration.yaml
- [ ] Home Assistant neu gestartet
- [ ] Developer Tools → Services zeigt pyscript.* Services

### Manuelle Installation (falls nötig)
- [ ] SSH oder Container Terminal verfügbar
- [ ] `pip install requests pyyaml` ausgeführt
- [ ] `python3 -c "import requests, yaml; print('OK')"` erfolgreich
- [ ] Home Assistant neu gestartet
- [ ] Import-Fehler in Logs prüfen

---

## 🎯 Typischer Setup-Flow

```
1. HACS installieren
   ↓
2. PyScript via HACS installieren
   ↓
3. configuration.yaml anpassen
   pyscript:
     allow_all_imports: true
   ↓
4. Home Assistant neu starten
   ↓
5. Developer Tools checken
   Services → pyscript.* sichtbar?
   ↓
6. PyScript File erstellen
   /config/pyscript/tuya_client.py
   ↓
7. Credentials eintragen
   ↓
8. Nochmal neu starten
   ↓
9. Fertig! Services sind verfügbar ✓
```

---

## 💡 Pro-Tipps

### Tip 1: Logs monitoren
```
tail -f /config/logs/home-assistant.log | grep pyscript
```

### Tip 2: Alle PyScript Services aufzählen
```
Developer Tools → Services
Suche: "pyscript"
→ Alle verfügbaren Services anzeigen
```

### Tip 3: PyScript Reload
```
Developer Tools → Services
Service: "PyScript: Reload"
```

### Tip 4: Debug Mode
```yaml
pyscript:
  allow_all_imports: true
  file_reloader: true
  hass_is_global: true
```

---

## 🔗 Hilfreiches

**Home Assistant Docs:**
- https://www.home-assistant.io/

**PyScript Docs:**
- https://hacs-pyscript.readthedocs.io/

**HACS Docs:**
- https://www.hacs.xyz/

**Python pip Docs:**
- https://pip.pypa.io/

---

## ✨ Zusammenfassung

**Einfach:**
1. HACS installieren
2. PyScript via HACS installieren
3. `allow_all_imports: true` in config.yaml
4. Neu starten
5. **Fertig!**

**Dependencies werden automatisch geladen.**

Bei Problemen: SSH Terminal → `pip install requests pyyaml` → Neu starten
