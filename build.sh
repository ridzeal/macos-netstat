#!/bin/bash
# Build script for MacOS NetStat standalone macOS app

set -e

echo "Building MacOS NetStat..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

VENV_BIN="./venv/bin"

# Install dependencies
echo "Installing dependencies..."
$VENV_BIN/pip install -r requirements.txt
$VENV_BIN/pip install py2app

# Clean previous build
echo "Cleaning previous build..."
rm -rf build dist

# Build the app
echo "Building app..."
$VENV_BIN/python setup.py py2app -A

echo ""
echo "Build complete! App is located at: dist/NetStat.app"
echo ""
echo "Note: This is an alias build for local development only."
echo "      The app requires Python to be installed on this machine."
echo ""
echo "To install locally:"
echo "  1. Copy dist/NetStat.app to /Applications"
echo "  2. Launch from Applications"
echo "  3. Add to login items in System Settings > General > Login Items"
echo ""
echo "For a distributable standalone app, install Homebrew Python"
echo "and rebuild without the -A flag."
