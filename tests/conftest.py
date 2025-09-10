"""
Pytest configuration for Tabletop Notetaker
"""

import sys
from pathlib import Path

# Add src to Python path for all tests
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Make pytest aware of the src directory
def pytest_configure(config):
    config.addinivalue_line("pythonpath", str(src_path))
