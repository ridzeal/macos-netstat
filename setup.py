"""
Setup script for building standalone macOS app using py2app.

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': None,  # Add path to .icns file if you create one
    'plist': {
        'CFBundleName': 'NetStat',
        'CFBundleDisplayName': 'NetStat',
        'CFBundleIdentifier': 'com.macosnetstat.netstat',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Run as menu bar app (no dock icon)
    },
    'packages': ['rumps', 'requests', 'psutil'],
}

setup(
    name='NetStat',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'rumps>=0.4.0',
        'requests>=2.31.0',
        'psutil>=5.9.0',
    ],
)
