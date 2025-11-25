@echo off
REM TUYA Smart Home Client - CLI Launcher
REM Startet die command-line Steuerung

echo.
echo ===================================================
echo  TUYA SMART HOME CLIENT - COMMAND LINE
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

REM Starte CLI
echo [*] Starte Steuerung...
python tuya_control.py

if errorlevel 1 (
    echo.
    echo [X] Fehler bei der Ausführung!
    echo Bitte prüfen Sie die Ausgabe oben.
    pause
)
