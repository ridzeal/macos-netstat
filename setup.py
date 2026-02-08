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
    'iconfile': 'NetStat.icns',
    'plist': {
        'CFBundleName': 'NetStat',
        'CFBundleDisplayName': 'NetStat',
        'CFBundleIdentifier': 'com.macosnetstat.netstat',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Run as menu bar app (no dock icon)
    },
    'packages': ['rumps', 'requests', 'psutil'],
    'site_packages': True,
}

setup(
    name='NetStat',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
