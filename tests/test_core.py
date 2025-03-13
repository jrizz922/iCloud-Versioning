"""Tests for the core functionality."""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

from icloud_versioning.core import VersionManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_file(temp_dir):
    """Create a test file in the temporary directory."""
    file_path = Path(temp_dir) / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Initial content")
    return file_path


def test_initialize(temp_dir):
    """Test initializing version tracking."""
    manager = VersionManager(temp_dir)
    manager.initialize()
    
    version_dir = Path(temp_dir) / ".versions"
    config_file = version_dir / "config.json"
    
    assert version_dir.exists()
    assert config_file.exists()


def test_track_file(temp_dir, test_file):
    """Test tracking a file."""
    manager = VersionManager(temp_dir)
    manager.initialize()
    manager.track_file(test_file)
    
    rel_path = test_file.relative_to(temp_dir)
    assert str(rel_path) in manager.config["tracked_files"]
    assert len(manager.config["tracked_files"][str(rel_path)]["versions"]) == 1


def test_get_status(temp_dir, test_file):
    """Test getting status of tracked files."""
    manager = VersionManager(temp_dir)
    manager.initialize()
    manager.track_file(test_file)
    
    status = manager.get_status()
    rel_path = str(test_file.relative_to(temp_dir))
    
    assert rel_path in status
    assert status[rel_path]["status"] == "unchanged"
    
    # Modify the file
    with open(test_file, "w") as f:
        f.write("Modified content")
    
    status = manager.get_status()
    assert status[rel_path]["status"] == "modified"


def test_restore_file(temp_dir, test_file):
    """Test restoring a file to a previous version."""
    manager = VersionManager(temp_dir)
    manager.initialize()
    manager.track_file(test_file)
    
    # Modify the file
    with open(test_file, "w") as f:
        f.write("Modified content")
    
    # Track the modified version
    manager.track_file(test_file)
    
    # Restore to the first version
    manager.restore_file(test_file, 1)
    
    with open(test_file, "r") as f:
        content = f.read()
    
    assert content == "Initial content"