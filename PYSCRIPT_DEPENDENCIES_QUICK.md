# PyScript Dependencies - Quick Reference Card 🚀

## 30 Sekunden Setup

### Automatisch (Empfohlen)

```yaml
# 1. configuration.yaml
pyscript:
  allow_all_imports: true    # ← This is it!

# 2. Restart Home Assistant
# 3. Done!
```

**Fertig! Dependencies werden automatisch geladen.**

---

## Was wird heruntergeladen?

```
requests  → HTTP Requests zu Tuya API
pyyaml    → YAML Dateien lesen
(rest ist in Python enthalten)
```

---

## Typische Fehler & Lösungen

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `ModuleNotFoundError: requests` | `allow_all_imports` nicht gesetzt | Setze auf `true` in config.yaml |
| Services nicht sichtbar | Dependencies nicht geladen | Restart HA nach config change |
| `pip: command not found` | SSH nicht verfügbar | Nutze SSH Add-on oder Docker |
| Import Error in Logs | Dependency nicht installiert | SSH: `pip install requests pyyaml` |

---

## Überprüfung

### Methode 1: Services checken
```
Developer Tools → Services
Suche: "pyscript"
Sollte Services zeigen ✓
```

### Methode 2: Logs checken
```
Einstellungen → System → Logs
Suche: "pyscript"
Sollte keine Fehler zeigen ✓
```

### Methode 3: SSH Terminal
```bash
python3 -c "import requests, yaml; print('✓ OK')"
```

---

## Manuelle Installation (Falls nötig)

### SSH Terminal
```bash
pip install requests pyyaml
```

### Docker
```bash
docker exec homeassistant pip install requests pyyaml
```

### Terminal Add-on
```
Settings → Add-ons → Terminal & SSH → Open Web terminal
pip install requests pyyaml
```

---

## Setup Flow

```
1. HACS installieren
   ↓
2. PyScript via HACS installieren
   ↓
3. configuration.yaml:
   pyscript:
     allow_all_imports: true
   ↓
4. Home Assistant neu starten
   ↓
5. ✓ Fertig!
```

---

## Vollständige Anleitung

📖 Siehe: `docs/PYSCRIPT_DEPENDENCIES.md`

