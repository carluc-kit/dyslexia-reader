# Dyslexia Reader 📖

Text-to-speech menu bar app with granular speed control. Select text anywhere on your Mac and have it read aloud.

## Features

- **Read selected text** from any app
- **Granular speed control** (0.5x to 2.0x in small increments)
- **Multiple voices** (8 different voices)
- **Menu bar app** - always accessible
- **Local processing** - no internet required after setup

## Installation

### 1. Install dependencies

```bash
# Install ffmpeg (for speed adjustment)
brew install ffmpeg

# Install Python packages
pip install rumps pyperclip pocket-tts
```

### 2. Grant Accessibility permissions

The app needs permission to simulate Cmd+C to copy selected text:

1. Open **System Preferences → Security & Privacy → Privacy → Accessibility**
2. Add **Terminal** (or your terminal app) and **Python** to the list
3. If running as an app, add the app itself

### 3. Run the app

```bash
python reader.py
```

You'll see a 📖 icon appear in your menu bar.

## Usage

1. **Select text** in any application
2. **Click the 📖 menu bar icon** → "Read Selected Text"
3. The text will be read aloud at your chosen speed

### Changing Speed

Click the menu bar icon → **Speed** → select your preferred speed (0.5x to 2.0x)

### Changing Voice

Click the menu bar icon → **Voice** → select a voice:
- Alba (default)
- Marius
- Javert
- Jean
- Fantine
- Cosette
- Eponine
- Azelma

## Running at Login

To start automatically when you log in:

1. Open **System Preferences → Users & Groups → Login Items**
2. Click **+** and add the `reader.py` script (or create an Automator app wrapper)

### Creating an App (optional)

To make a proper .app bundle:

```bash
pip install py2app
python setup.py py2app
```

Then move `dist/Dyslexia Reader.app` to your Applications folder.

## Troubleshooting

### "No Text Selected" error
- Make sure text is actually selected (highlighted)
- Try selecting text again and wait a moment before clicking Read

### No sound
- Check your volume
- Make sure `ffmpeg` is installed: `brew install ffmpeg`
- Check Terminal/Python has Accessibility permissions

### First run is slow
- The TTS model (~100MB) downloads on first use
- Subsequent runs are faster

## Technical Details

- Uses [Kyutai Pocket TTS](https://github.com/kyutai-labs/pocket-tts) for speech synthesis
- Speed adjustment via ffmpeg's atempo filter
- Runs entirely locally - no cloud APIs
