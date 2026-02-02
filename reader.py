#!/usr/bin/env python3
"""
Dyslexia Reader - Text-to-Speech with granular speed control
Menu bar app that reads selected text aloud.

Requirements:
    pip install rumps pyperclip

Usage:
    python reader.py
    
Then select text anywhere and press Cmd+Shift+R (or click the menu bar icon)
"""

import subprocess
import tempfile
import os
import threading
import rumps
from pathlib import Path

# Try to import pyperclip, fall back to pbpaste if not available
try:
    import pyperclip
    def get_clipboard():
        return pyperclip.paste()
except ImportError:
    def get_clipboard():
        return subprocess.run(['pbpaste'], capture_output=True, text=True).stdout


class DyslexiaReaderApp(rumps.App):
    def __init__(self):
        super().__init__("📖", quit_button=None)
        
        # Settings
        self.speed = 1.0
        self.voice = "alba"
        self.voices = ["alba", "marius", "javert", "jean", "fantine", "cosette", "eponine", "azelma"]
        
        # Build menu
        self.menu = [
            rumps.MenuItem("Read Selected Text (⌘⇧R)", callback=self.read_selection),
            None,  # Separator
            self._build_speed_menu(),
            self._build_voice_menu(),
            None,
            rumps.MenuItem("Quit", callback=rumps.quit_application),
        ]
        
        # Register global hotkey
        self._register_hotkey()
    
    def _build_speed_menu(self):
        speed_menu = rumps.MenuItem("Speed")
        speeds = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.3, 1.5, 1.75, 2.0]
        for s in speeds:
            item = rumps.MenuItem(f"{s}x", callback=self._make_speed_callback(s))
            if s == self.speed:
                item.state = 1
            speed_menu.add(item)
        return speed_menu
    
    def _make_speed_callback(self, speed):
        def callback(sender):
            self.speed = speed
            # Update checkmarks
            for item in self.menu["Speed"].values():
                item.state = 1 if item.title == f"{speed}x" else 0
            rumps.notification("Speed Changed", "", f"Reading speed set to {speed}x")
        return callback
    
    def _build_voice_menu(self):
        voice_menu = rumps.MenuItem("Voice")
        for v in self.voices:
            item = rumps.MenuItem(v.capitalize(), callback=self._make_voice_callback(v))
            if v == self.voice:
                item.state = 1
            voice_menu.add(item)
        return voice_menu
    
    def _make_voice_callback(self, voice):
        def callback(sender):
            self.voice = voice
            # Update checkmarks
            for item in self.menu["Voice"].values():
                item.state = 1 if item.title == voice.capitalize() else 0
            rumps.notification("Voice Changed", "", f"Voice set to {voice.capitalize()}")
        return callback
    
    def _register_hotkey(self):
        """Register Cmd+Shift+R as global hotkey using AppleScript"""
        # Note: For true global hotkeys, you'd need to use Accessibility APIs
        # This is a simplified version - the menu bar provides the main interface
        pass
    
    def get_selected_text(self):
        """Get currently selected text by simulating Cmd+C"""
        # Store current clipboard
        old_clipboard = get_clipboard()
        
        # Simulate Cmd+C
        script = 'tell application "System Events" to keystroke "c" using command down'
        subprocess.run(['osascript', '-e', script], capture_output=True)
        
        # Small delay for clipboard to update
        import time
        time.sleep(0.1)
        
        # Get new clipboard content
        text = get_clipboard()
        
        # Restore old clipboard (optional - comment out if you want to keep the copy)
        # pyperclip.copy(old_clipboard)
        
        return text if text != old_clipboard else text
    
    @rumps.clicked("Read Selected Text (⌘⇧R)")
    def read_selection(self, _):
        """Read the currently selected text"""
        text = self.get_selected_text()
        
        if not text or not text.strip():
            rumps.notification("No Text Selected", "", "Please select some text first")
            return
        
        # Show notification
        preview = text[:50] + "..." if len(text) > 50 else text
        rumps.notification("Reading...", f"Speed: {self.speed}x | Voice: {self.voice}", preview)
        
        # Generate and play in background thread
        threading.Thread(target=self._generate_and_play, args=(text,), daemon=True).start()
    
    def _generate_and_play(self, text):
        """Generate TTS audio and play it"""
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                raw_path = os.path.join(tmpdir, "raw.wav")
                final_path = os.path.join(tmpdir, "final.wav")
                
                # Generate with pocket-tts
                result = subprocess.run(
                    ["uvx", "pocket-tts", "generate", 
                     "--text", text, 
                     "--voice", self.voice,
                     "--output-path", raw_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    rumps.notification("Error", "TTS generation failed", result.stderr[:100])
                    return
                
                # Adjust speed with ffmpeg if not 1.0x
                if self.speed != 1.0:
                    # atempo filter only accepts 0.5-2.0, chain for extreme values
                    atempo_filters = []
                    remaining_speed = self.speed
                    
                    while remaining_speed < 0.5:
                        atempo_filters.append("atempo=0.5")
                        remaining_speed /= 0.5
                    while remaining_speed > 2.0:
                        atempo_filters.append("atempo=2.0")
                        remaining_speed /= 2.0
                    atempo_filters.append(f"atempo={remaining_speed}")
                    
                    filter_str = ",".join(atempo_filters)
                    
                    subprocess.run(
                        ["ffmpeg", "-y", "-i", raw_path, 
                         "-filter:a", filter_str, 
                         final_path],
                        capture_output=True
                    )
                    play_path = final_path
                else:
                    play_path = raw_path
                
                # Play with afplay (macOS built-in)
                subprocess.run(["afplay", play_path])
                
        except Exception as e:
            rumps.notification("Error", "Playback failed", str(e)[:100])


if __name__ == "__main__":
    DyslexiaReaderApp().run()
