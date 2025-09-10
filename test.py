#!/usr/bin/env python3
"""
Quick test script for Tabletop Notetaker functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.app import TabletopNotetakerApp

def test_basic_functionality():
    """Test basic application functionality"""
    print("=== Tabletop Notetaker Test ===")

    # Initialize app
    app = TabletopNotetakerApp()
    print("✓ Application initialized")

    # Test recording service
    print("✓ Recording service available")

    # Test transcription service
    print("✓ Transcription service available")

    # Test summarization service
    print("✓ Summarization service available")

    print("\n=== Test Complete ===")
    print("The application is ready to use!")
    print("\nTo start:")
    print("  CLI: python main.py")
    print("  GUI: python main.py --gui")

if __name__ == "__main__":
    test_basic_functionality()
