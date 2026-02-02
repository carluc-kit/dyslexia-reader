#!/usr/bin/env python3
"""
Simple TTS script - reads text from argument or stdin

Usage:
    python speak.py "Text to read"
    echo "Text to read" | python speak.py
    pbpaste | python speak.py  # Read clipboard on macOS

Options (via environment variables):
    SPEED=0.85 python speak.py "text"
    VOICE=marius python speak.py "text"
"""

import sys
import subprocess
import tempfile
import os

# Config - change these or use environment variables
SPEED = float(os.environ.get("SPEED", "0.85"))
VOICE = os.environ.get("VOICE", "alba")


def speak(text: str, speed: float = SPEED, voice: str = VOICE):
    """Generate TTS and play audio"""
    if not text.strip():
        print("No text provided", file=sys.stderr)
        return
    
    with tempfile.TemporaryDirectory() as tmpdir:
        raw_path = os.path.join(tmpdir, "raw.wav")
        final_path = os.path.join(tmpdir, "final.wav")
        
        # Generate with pocket-tts
        print(f"Generating speech... (voice={voice}, speed={speed}x)", file=sys.stderr)
        result = subprocess.run(
            ["uvx", "pocket-tts", "generate",
             "--text", text,
             "--voice", voice,
             "--output-path", raw_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"TTS error: {result.stderr}", file=sys.stderr)
            return
        
        # Adjust speed with ffmpeg
        if speed != 1.0:
            # Build atempo filter chain (atempo only accepts 0.5-2.0)
            atempo_filters = []
            remaining = speed
            
            while remaining < 0.5:
                atempo_filters.append("atempo=0.5")
                remaining /= 0.5
            while remaining > 2.0:
                atempo_filters.append("atempo=2.0")
                remaining /= 2.0
            atempo_filters.append(f"atempo={remaining}")
            
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
        
        # Play audio
        print("Playing...", file=sys.stderr)
        subprocess.run(["afplay", play_path])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Text from command line argument
        text = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        # Text from stdin
        text = sys.stdin.read()
    else:
        print("Usage: python speak.py 'text to speak'", file=sys.stderr)
        print("   or: echo 'text' | python speak.py", file=sys.stderr)
        print("   or: pbpaste | python speak.py", file=sys.stderr)
        sys.exit(1)
    
    speak(text)
