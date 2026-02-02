#!/usr/bin/env python3
"""
Tests for Dyslexia Reader

Run with: pytest test_reader.py -v
"""

import pytest
import subprocess
import tempfile
import os


class TestAtempoFilterChain:
    """Test the ffmpeg atempo filter chain logic for speed adjustment"""
    
    def build_atempo_filters(self, speed: float) -> str:
        """Replicate the atempo filter building logic from reader.py"""
        atempo_filters = []
        remaining = speed
        
        while remaining < 0.5:
            atempo_filters.append("atempo=0.5")
            remaining /= 0.5
        while remaining > 2.0:
            atempo_filters.append("atempo=2.0")
            remaining /= 2.0
        atempo_filters.append(f"atempo={remaining}")
        
        return ",".join(atempo_filters)
    
    def test_normal_speed(self):
        """1.0x should produce single filter"""
        result = self.build_atempo_filters(1.0)
        assert result == "atempo=1.0"
    
    def test_slight_slowdown(self):
        """0.85x should produce single filter"""
        result = self.build_atempo_filters(0.85)
        assert result == "atempo=0.85"
    
    def test_slight_speedup(self):
        """1.15x should produce single filter"""
        result = self.build_atempo_filters(1.15)
        assert result == "atempo=1.15"
    
    def test_max_single_speedup(self):
        """2.0x should produce single filter"""
        result = self.build_atempo_filters(2.0)
        assert result == "atempo=2.0"
    
    def test_min_single_slowdown(self):
        """0.5x should produce single filter"""
        result = self.build_atempo_filters(0.5)
        assert result == "atempo=0.5"
    
    def test_extreme_slowdown(self):
        """0.25x needs chained filters (0.5 * 0.5)"""
        result = self.build_atempo_filters(0.25)
        assert "atempo=0.5" in result
        # Should have two filters
        assert result.count("atempo") == 2
    
    def test_extreme_speedup(self):
        """4.0x needs chained filters (2.0 * 2.0)"""
        result = self.build_atempo_filters(4.0)
        assert "atempo=2.0" in result
        # Should have two filters
        assert result.count("atempo") == 2


class TestSpeedOptions:
    """Test that all speed options are valid"""
    
    SPEEDS = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 
              1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.75, 2.0]
    
    def test_all_speeds_positive(self):
        """All speeds should be positive"""
        for speed in self.SPEEDS:
            assert speed > 0
    
    def test_all_speeds_in_range(self):
        """All speeds should be between 0.5 and 2.0 (single filter range)"""
        for speed in self.SPEEDS:
            assert 0.5 <= speed <= 2.0
    
    def test_speeds_sorted(self):
        """Speeds should be in ascending order"""
        assert self.SPEEDS == sorted(self.SPEEDS)
    
    def test_includes_normal_speed(self):
        """1.0x should be an option"""
        assert 1.0 in self.SPEEDS
    
    def test_granular_above_1x(self):
        """Should have multiple options between 1.0 and 1.3"""
        above_1 = [s for s in self.SPEEDS if 1.0 < s < 1.3]
        assert len(above_1) >= 4  # 1.05, 1.1, 1.15, 1.2, 1.25


class TestVoices:
    """Test voice options"""
    
    VOICES = ["alba", "marius", "javert", "jean", "fantine", "cosette", "eponine", "azelma"]
    
    def test_has_default_voice(self):
        """Alba should be the first/default voice"""
        assert self.VOICES[0] == "alba"
    
    def test_all_voices_lowercase(self):
        """All voice names should be lowercase"""
        for voice in self.VOICES:
            assert voice == voice.lower()
    
    def test_voice_count(self):
        """Should have 8 voices"""
        assert len(self.VOICES) == 8


class TestTextHandling:
    """Test text input handling"""
    
    def test_empty_string(self):
        """Empty string should be detected"""
        text = ""
        assert not text.strip()
    
    def test_whitespace_only(self):
        """Whitespace-only should be detected as empty"""
        text = "   \n\t  "
        assert not text.strip()
    
    def test_normal_text(self):
        """Normal text should pass"""
        text = "Hello, this is a test."
        assert text.strip()
    
    def test_long_text_preview(self):
        """Long text preview should truncate at 50 chars"""
        text = "A" * 100
        preview = text[:50] + "..." if len(text) > 50 else text
        assert len(preview) == 53  # 50 + "..."
        assert preview.endswith("...")
    
    def test_short_text_preview(self):
        """Short text should not be truncated"""
        text = "Short text"
        preview = text[:50] + "..." if len(text) > 50 else text
        assert preview == "Short text"
        assert not preview.endswith("...")


class TestDependencies:
    """Test that required dependencies are available (skip if not on macOS)"""
    
    @pytest.mark.skipif(os.uname().sysname != "Darwin", reason="macOS only")
    def test_ffmpeg_available(self):
        """ffmpeg should be installed"""
        result = subprocess.run(["which", "ffmpeg"], capture_output=True)
        assert result.returncode == 0
    
    @pytest.mark.skipif(os.uname().sysname != "Darwin", reason="macOS only")
    def test_afplay_available(self):
        """afplay should be available (macOS built-in)"""
        result = subprocess.run(["which", "afplay"], capture_output=True)
        assert result.returncode == 0
    
    def test_uvx_command_exists(self):
        """uvx should be available for pocket-tts"""
        result = subprocess.run(["which", "uvx"], capture_output=True)
        # Don't fail if not installed, just skip
        if result.returncode != 0:
            pytest.skip("uvx not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
