"""
Setup script for creating a macOS .app bundle

Usage:
    pip install py2app
    python setup.py py2app
    
The app will be in dist/Dyslexia Reader.app
"""

from setuptools import setup

APP = ['reader.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'Dyslexia Reader',
        'CFBundleDisplayName': 'Dyslexia Reader',
        'CFBundleIdentifier': 'com.dyslexia.reader',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # Makes it a menu bar only app (no dock icon)
        'NSAccessibilityUsageDescription': 'Dyslexia Reader needs accessibility access to read selected text from other applications.',
    },
    'packages': ['rumps'],
    'includes': ['pyperclip'],
}

setup(
    name='Dyslexia Reader',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
