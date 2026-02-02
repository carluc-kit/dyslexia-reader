#!/bin/bash
# Dyslexia Reader - One-line installer for macOS
# Usage: curl -fsSL https://raw.githubusercontent.com/carluc-kit/dyslexia-reader/main/install.sh | bash

set -e

echo "📖 Installing Dyslexia Reader..."

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install ffmpeg
echo "Installing ffmpeg..."
brew install ffmpeg 2>/dev/null || true

# Install uv if not present (faster than pip)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create app directory
APP_DIR="$HOME/.local/share/dyslexia-reader"
mkdir -p "$APP_DIR"

# Download the app
echo "Downloading Dyslexia Reader..."
curl -fsSL https://raw.githubusercontent.com/carluc-kit/dyslexia-reader/main/reader.py -o "$APP_DIR/reader.py"
curl -fsSL https://raw.githubusercontent.com/carluc-kit/dyslexia-reader/main/speak.py -o "$APP_DIR/speak.py"

# Create a virtual environment and install deps
echo "Installing Python dependencies..."
cd "$APP_DIR"
uv venv .venv
uv pip install rumps pyperclip pocket-tts --quiet

# Create launcher script
cat > "$APP_DIR/run.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python reader.py
EOF
chmod +x "$APP_DIR/run.sh"

# Create macOS .app bundle
APP_BUNDLE="$HOME/Applications/Dyslexia Reader.app"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Create Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Dyslexia Reader</string>
    <key>CFBundleDisplayName</key>
    <string>Dyslexia Reader</string>
    <key>CFBundleIdentifier</key>
    <string>com.carluc-kit.dyslexia-reader</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleExecutable</key>
    <string>launch</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSAccessibilityUsageDescription</key>
    <string>Dyslexia Reader needs accessibility access to read selected text.</string>
</dict>
</plist>
EOF

# Create launcher
cat > "$APP_BUNDLE/Contents/MacOS/launch" << EOF
#!/bin/bash
"$APP_DIR/run.sh"
EOF
chmod +x "$APP_BUNDLE/Contents/MacOS/launch"

echo ""
echo "✅ Dyslexia Reader installed!"
echo ""
echo "📍 App location: ~/Applications/Dyslexia Reader.app"
echo ""
echo "To start:"
echo "  1. Open ~/Applications/Dyslexia Reader.app"
echo "  2. Grant Accessibility permission when prompted"
echo "  3. Look for 📖 in your menu bar"
echo ""
echo "First run downloads the TTS model (~100MB) - be patient!"
echo ""

# Ask to open now
read -p "Open Dyslexia Reader now? [Y/n] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    open "$HOME/Applications/Dyslexia Reader.app"
fi
