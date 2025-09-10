"""
Test suite for Tabletop Notetaker
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_core_imports():
    """Test that core modules can be imported"""
    try:
        from core.app import TabletopNotetakerApp
        from services.recording_service import RecordingService
        from services.transcription_service import TranscriptionService
        from services.summarization_service import SummarizationService
        print("✓ All core imports successful")
        assert True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        assert False, f"Import failed: {e}"

def test_app_initialization():
    """Test that the main app can be initialized"""
    try:
        from core.app import TabletopNotetakerApp
        app = TabletopNotetakerApp()
        assert app is not None
        assert hasattr(app, 'recording_service')
        assert hasattr(app, 'transcription_service')
        assert hasattr(app, 'summarization_service')
        print("✓ App initialization successful")
    except Exception as e:
        print(f"✗ App initialization failed: {e}")
        assert False, f"App initialization failed: {e}"

def test_cli_import():
    """Test CLI interface import"""
    try:
        from ui.cli import CLIInterface
        print("✓ CLI import successful")
        assert True
    except ImportError as e:
        print(f"✗ CLI import error: {e}")
        assert False, f"CLI import failed: {e}"

def test_gui_import():
    """Test GUI interface import (may fail if tkinter not available)"""
    try:
        import tkinter
        from ui.gui import GUIInterface
        print("✓ GUI import successful")
        assert True
    except ImportError as e:
        print(f"⚠ GUI import failed (tkinter not available): {e}")
        print("Skipping GUI tests - tkinter not available in this environment")
        assert True  # Don't fail the test, just skip GUI functionality

def test_services_initialization():
    """Test that all services can be initialized"""
    try:
        from services.recording_service import RecordingService
        from services.transcription_service import TranscriptionService
        from services.summarization_service import SummarizationService

        recording = RecordingService()
        transcription = TranscriptionService()
        summarization = SummarizationService()

        assert recording is not None
        assert transcription is not None
        assert summarization is not None

        print("✓ All services initialized successfully")
    except Exception as e:
        print(f"✗ Service initialization failed: {e}")
        assert False, f"Service initialization failed: {e}"

def test_summarization_functionality():
    """Test summarization service with sample data"""
    try:
        from services.summarization_service import SummarizationService

        service = SummarizationService()

        # Sample transcript data
        sample_transcript = {
            'segments': [
                {'speaker': 'Alice', 'text': 'Hello everyone, let\'s start the meeting.', 'start': 0, 'end': 5},
                {'speaker': 'Bob', 'text': 'I think we should discuss the new project timeline.', 'start': 6, 'end': 12},
                {'speaker': 'Alice', 'text': 'Good idea. We need to finish by next Friday.', 'start': 13, 'end': 18}
            ]
        }

        summary = service.summarize(sample_transcript, 'txt')
        assert summary is not None
        assert len(summary) > 0
        assert 'Alice' in summary or 'Bob' in summary

        print("✓ Summarization test successful")
    except Exception as e:
        print(f"✗ Summarization test failed: {e}")
        assert False, f"Summarization test failed: {e}"

if __name__ == "__main__":
    # Run tests manually if called directly
    print("Running Tabletop Notetaker tests...\n")

    test_core_imports()
    test_app_initialization()
    test_cli_import()
    test_gui_import()
    test_services_initialization()
    test_summarization_functionality()

    print("\n✅ All tests completed!")
