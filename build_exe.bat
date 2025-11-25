@echo off
REM Build Tuya Client EXE with PyInstaller
REM Creates standalone executable

echo ============================================
echo Tuya Cloud Client - Build EXE
echo ============================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo.
echo Building GUI EXE...
echo.

REM Build GUI EXE
pyinstaller ^
    --name "Tuya-Client-GUI" ^
    --onefile ^
    --windowed ^
    --add-data "config.yaml:." ^
    tuya_gui.py

if errorlevel 1 (
    echo Error building GUI EXE!
    pause
    exit /b 1
)

echo.
echo Building CLI EXE...
echo.

REM Build CLI EXE
pyinstaller ^
    --name "Tuya-Client-CLI" ^
    --onefile ^
    --console ^
    --add-data "config.yaml:." ^
    tuya_control.py

if errorlevel 1 (
    echo Error building CLI EXE!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Build completed successfully!
echo ============================================
echo.
echo Output location:
echo   GUI: dist\Tuya-Client-GUI.exe
echo   CLI: dist\Tuya-Client-CLI.exe
echo.
echo Before distribution:
echo 1. Copy config.yaml to the dist folder
echo 2. Test both EXEs on a clean system
echo 3. Create a release ZIP
echo.
pause
