#!/usr/bin/env python3
"""
Simple test runner for Tabletop Notetaker (works without pytest)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def run_tests():
    """Run all tests manually"""
    print("Running Tabletop Notetaker tests...\n")

    test_functions = [
        test_core_imports,
        test_app_initialization,
        test_cli_import,
        test_gui_import,
        test_services_initialization,
        test_summarization_functionality
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            print(f"Running {test_func.__name__}...")
            test_func()
            print(f"✓ {test_func.__name__} PASSED\n")
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} FAILED: {e}\n")
            failed += 1

    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0

def test_core_imports():
    """Test that core modules can be imported"""
    from core.app import TabletopNotetakerApp
    from services.recording_service import RecordingService
    from services.transcription_service import TranscriptionService
    from services.summarization_service import SummarizationService

def test_app_initialization():
    """Test that the main app can be initialized"""
    from core.app import TabletopNotetakerApp
    app = TabletopNotetakerApp()
    assert app is not None
    assert hasattr(app, 'recording_service')
    assert hasattr(app, 'transcription_service')
    assert hasattr(app, 'summarization_service')

def test_cli_import():
    """Test CLI interface import"""
    from ui.cli import CLIInterface

def test_gui_import():
    """Test GUI interface import (may fail if tkinter not available)"""
    try:
        import tkinter
        from ui.gui import GUIInterface
    except ImportError:
        print("GUI not available (tkinter not found) - skipping GUI tests")
        # Don't raise exception, just skip

def test_services_initialization():
    """Test that all services can be initialized"""
    from services.recording_service import RecordingService
    from services.transcription_service import TranscriptionService
    from services.summarization_service import SummarizationService

    recording = RecordingService()
    transcription = TranscriptionService()
    summarization = SummarizationService()

    assert recording is not None
    assert transcription is not None
    assert summarization is not None

def test_summarization_functionality():
    """Test summarization service with sample data"""
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

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
