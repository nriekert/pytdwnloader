@echo off


echo Installing dependencies

pip install pyinstaller
pip install yt-dlp

echo Building pytdwnloader GUI...
echo.

timeout /t 3 /nobreak > nul

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build using spec file
pyinstaller pytdwnloader_gui.spec
pyinstaller pytdwnloader.spec

echo.
echo Build completed! Check the dist folder for the executable.
pause
