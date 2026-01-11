#!/bin/bash
echo Installing dependencies

pip install pyinstaller
pip install yt-dlp

echo Cleaning previous builds

rm -rf build dist

echo "Building pytdwnloader GUI..."
echo.
timeout 3

pyinstaller pytdwnloader_gui.spec

echo
echo "Build complete! Check the dist folder for the executable."
