# Dyslexia Reader 📖

Text-to-speech menu bar app for macOS with granular speed control. Select text anywhere and have it read aloud.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/carluc-kit/dyslexia-reader/main/install.sh | bash
```

That's it! The installer:
- Installs dependencies (Homebrew, ffmpeg, Python packages)
- Creates an app in ~/Applications
- First run downloads the TTS model (~100MB)

## Usage

1. Open **Dyslexia Reader** from ~/Applications
2. Grant **Accessibility permission** when prompted
3. **Select text** anywhere on your Mac
4. Click **📖** in the menu bar → **Read Selected Text**

### Speed Control

Click 📖 → **Speed** → choose from 0.5x to 2.0x

Recommended for dyslexia: **0.75x - 0.85x**

### Voices

8 voices available: Alba (default), Marius, Javert, Jean, Fantine, Cosette, Eponine, Azelma

## Features

- ✅ Granular speed control (0.5x to 2.0x)
- ✅ Multiple natural voices
- ✅ Works with any app
- ✅ 100% local - no internet needed after install
- ✅ Privacy-focused - your text never leaves your Mac

## Troubleshooting

**"No Text Selected"** - Make sure text is highlighted before clicking Read

**No sound** - Check volume, ensure ffmpeg is installed (`brew install ffmpeg`)

**Permission denied** - Go to System Settings → Privacy & Security → Accessibility → enable Dyslexia Reader

## Uninstall

```bash
rm -rf ~/Applications/Dyslexia\ Reader.app
rm -rf ~/.local/share/dyslexia-reader
```
