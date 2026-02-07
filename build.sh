#!/bin/bash
# Build script for MacOS NetStat standalone macOS app

set -e

echo "Building MacOS NetStat..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install py2app

# Clean previous build
echo "Cleaning previous build..."
rm -rf build dist

# Build the app
echo "Building app..."
python setup.py py2app

echo ""
echo "Build complete! App is located in: dist/NetStat.app"
echo ""
echo "To install:"
echo "  1. Copy dist/NetStat.app to /Applications"
echo "  2. Launch from Applications"
echo "  3. Add to login items in System Settings > General > Login Items"
echo ""
echo "Note: On first run, you may need to right-click and 'Open' to bypass"
echo "      Gatekeeper since the app is unsigned."
