#!/usr/bin/env python3
"""Convenience launcher for agentic-quorum without needing PYTHONPATH or installation."""

import os
import sys
from pathlib import Path

# Add src to sys.path automatically
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from agentic_quorum.cli import main

if __name__ == "__main__":
    sys.exit(main())
