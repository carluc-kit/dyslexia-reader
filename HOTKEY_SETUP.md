# Setting Up a Global Hotkey

The menu bar app works great, but if you want a true global hotkey (like ⌘⇧R from anywhere), here are your options:

## Option 1: macOS Shortcuts (Easiest)

1. Open **Shortcuts** app
2. Create new shortcut
3. Add action: **Run Shell Script**
4. Paste this script:
   ```bash
   # Copy selected text
   osascript -e 'tell application "System Events" to keystroke "c" using command down'
   sleep 0.1
   
   # Get clipboard and read it
   TEXT=$(pbpaste)
   if [ -n "$TEXT" ]; then
       cd /path/to/dyslexia-reader
       python -c "
   import subprocess, tempfile, os
   text = '''$TEXT'''
   speed = 0.85  # Adjust this!
   voice = 'alba'
   
   with tempfile.TemporaryDirectory() as tmpdir:
       raw = os.path.join(tmpdir, 'raw.wav')
       final = os.path.join(tmpdir, 'final.wav')
       subprocess.run(['uvx', 'pocket-tts', 'generate', '--text', text, '--voice', voice, '--output-path', raw])
       subprocess.run(['ffmpeg', '-y', '-i', raw, '-filter:a', f'atempo={speed}', final], capture_output=True)
       subprocess.run(['afplay', final])
   "
   fi
   ```
5. Click **Shortcut Details** (ⓘ) → **Add Keyboard Shortcut** → press ⌘⇧R

## Option 2: Automator Quick Action

1. Open **Automator** → New → **Quick Action**
2. Set "Workflow receives" to **no input** in **any application**
3. Add **Run Shell Script** action with the script above
4. Save as "Read Selected Text"
5. Go to **System Preferences → Keyboard → Shortcuts → Services**
6. Find your action and assign ⌘⇧R

## Option 3: Hammerspoon (Power User)

Install [Hammerspoon](https://www.hammerspoon.org/) and add to `~/.hammerspoon/init.lua`:

```lua
hs.hotkey.bind({"cmd", "shift"}, "R", function()
    -- Copy selection
    hs.eventtap.keyStroke({"cmd"}, "c")
    hs.timer.usleep(100000)
    
    -- Get clipboard
    local text = hs.pasteboard.getContents()
    if text and text ~= "" then
        -- Run TTS (adjust path)
        hs.task.new("/usr/bin/python3", nil, {
            "/path/to/dyslexia-reader/speak.py",
            text
        }):start()
    end
end)
```

Then create `speak.py`:
```python
#!/usr/bin/env python3
import sys
import subprocess
import tempfile
import os

text = sys.argv[1] if len(sys.argv) > 1 else ""
speed = 0.85  # Adjust!
voice = "alba"

if text:
    with tempfile.TemporaryDirectory() as tmpdir:
        raw = os.path.join(tmpdir, "raw.wav")
        final = os.path.join(tmpdir, "final.wav")
        subprocess.run(["uvx", "pocket-tts", "generate", "--text", text, "--voice", voice, "--output-path", raw])
        subprocess.run(["ffmpeg", "-y", "-i", raw, "-filter:a", f"atempo={speed}", final], capture_output=True)
        subprocess.run(["afplay", final])
```

## Quick Speed Reference

For dyslexia, slower speeds often work better:
- **0.7x** - Very slow, good for dense technical text
- **0.8x** - Slow, comfortable for most reading
- **0.85x** - Slightly slow (recommended starting point)
- **0.9x** - Almost normal
- **1.0x** - Normal speed
