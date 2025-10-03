#!/usr/bin/env python
"""
Cleanup script for Agent Zero project.
Removes Python cache files and other temporary artifacts.
"""

import os
import shutil
from pathlib import Path

def clean_caches(root_dir="."):
    """Remove Python cache directories and files."""
    print("Cleaning up Python cache files...")
    
    # Cache directories to remove
    cache_patterns = [
        "**/__pycache__",
        "**/.pytest_cache",
        "**/.ruff_cache",
        "**/.mypy_cache",
        "**/node_modules",
        "**/.coverage",
        "**/.ipynb_checkpoints",
    ]
    
    total_removed = 0
    
    for pattern in cache_patterns:
        for path in Path(root_dir).glob(pattern):
            if path.is_dir():
                print(f"Removing directory: {path}")
                shutil.rmtree(path)
                total_removed += 1
            elif path.is_file():
                print(f"Removing file: {path}")
                path.unlink()
                total_removed += 1
    
    # Remove specific file patterns
    file_patterns = [
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/*.so",
        "**/*.dll",
        "**/*.exe",
        "**/*.coverage",
        "**/*.coverage.*",
        "**/*.log",
        "**/pip-log.txt",
        "**/pip-delete-this-directory.txt",
    ]
    
    for pattern in file_patterns:
        for path in Path(root_dir).glob(pattern):
            if path.is_file() and not str(path).startswith(".git"):
                print(f"Removing file: {path}")
                path.unlink()
                total_removed += 1
    
    print(f"Cleanup complete. Removed {total_removed} files/directories.")

if __name__ == "__main__":
    clean_caches()