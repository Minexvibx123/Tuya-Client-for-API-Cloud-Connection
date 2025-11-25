@echo off
REM TUYA Smart Home Client - GUI Launcher
REM Startet die grafische Benutzeroberfläche

echo.
echo ===================================================
echo  TUYA SMART HOME CLIENT - GUI
echo ===================================================
echo.

cd /d "%~dp0"

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python nicht gefunden!
    echo Bitte installieren Sie Python 3.6+ und versuchen Sie es erneut.
    pause
    exit /b 1
)

REM Prüfe ob config.yaml existiert
if not exist "config.yaml" (
    echo [X] config.yaml nicht gefunden!
    echo Bitte erstellen Sie die Konfigurationsdatei.
    pause
    exit /b 1
)

REM Starte GUI
echo [*] Starte GUI...
python tuya_gui.py

if errorlevel 1 (
    echo.
    echo [X] Fehler beim Starten der GUI!
    echo Bitte prüfen Sie die Ausgabe oben.
    pause
)
