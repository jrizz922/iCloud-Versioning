"""Core functionality for iCloud Versioning."""

import os
import json
import shutil
import hashlib
from datetime import datetime
from pathlib import Path


class VersionManager:
    """Manages versioning for files in a directory."""

    def __init__(self, directory):
        """Initialize the version manager.
        
        Args:
            directory (str): Path to the directory to manage
        """
        self.directory = Path(directory)
        self.version_dir = self.directory / ".versions"
        self.config_file = self.version_dir / "config.json"
        self.config = self._load_config()

    def initialize(self):
        """Initialize version tracking in the directory."""
        if not self.version_dir.exists():
            self.version_dir.mkdir(exist_ok=True)
            
        if not self.config_file.exists():
            self.config = {
                "tracked_files": {},
                "initialized_at": datetime.now().isoformat(),
            }
            self._save_config()

    def track_file(self, file_path):
        """Start tracking a file.
        
        Args:
            file_path (str): Path to the file to track
        """
        file_path = Path(file_path)
        rel_path = file_path.relative_to(self.directory)
        file_hash = self._hash_file(file_path)
        
        if str(rel_path) not in self.config["tracked_files"]:
            self.config["tracked_files"][str(rel_path)] = {
                "versions": [],
                "added_at": datetime.now().isoformat(),
            }
        
        # Create a new version
        version_num = len(self.config["tracked_files"][str(rel_path)]["versions"]) + 1
        version_info = {
            "version": version_num,
            "hash": file_hash,
            "timestamp": datetime.now().isoformat(),
            "size": file_path.stat().st_size,
        }
        
        self.config["tracked_files"][str(rel_path)]["versions"].append(version_info)
        
        # Save the file
        version_file_dir = self.version_dir / str(rel_path).replace("/", "_")
        version_file_dir.mkdir(exist_ok=True, parents=True)
        version_file = version_file_dir / f"v{version_num}"
        shutil.copy2(file_path, version_file)
        
        self._save_config()

    def get_status(self):
        """Get status of tracked files.
        
        Returns:
            dict: Status information for tracked files
        """
        status = {}
        
        for rel_path, info in self.config["tracked_files"].items():
            file_path = self.directory / rel_path
            
            if not file_path.exists():
                status[rel_path] = {"status": "missing"}
                continue
                
            current_hash = self._hash_file(file_path)
            latest_version = info["versions"][-1]
            
            if current_hash == latest_version["hash"]:
                status[rel_path] = {"status": "unchanged"}
            else:
                status[rel_path] = {"status": "modified"}
                
        return status

    def restore_file(self, file_path, version=None):
        """Restore a file to a previous version.
        
        Args:
            file_path (str): Path to the file to restore
            version (int, optional): Version to restore. Defaults to the latest.
        """
        file_path = Path(file_path)
        rel_path = file_path.relative_to(self.directory)
        
        if str(rel_path) not in self.config["tracked_files"]:
            raise ValueError(f"File {file_path} is not being tracked")
            
        versions = self.config["tracked_files"][str(rel_path)]["versions"]
        
        if version is None:
            version = len(versions)
        elif version < 1 or version > len(versions):
            raise ValueError(f"Version {version} does not exist")
            
        version_file_dir = self.version_dir / str(rel_path).replace("/", "_")
        version_file = version_file_dir / f"v{version}"
        
        if not version_file.exists():
            raise FileNotFoundError(f"Version file {version_file} not found")
            
        # Backup current version if it differs from any stored version
        current_hash = self._hash_file(file_path)
        if not any(v["hash"] == current_hash for v in versions):
            self.track_file(file_path)
            
        # Restore the file
        shutil.copy2(version_file, file_path)

    def _hash_file(self, file_path):
        """Calculate the hash of a file.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            str: SHA-256 hash of the file
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _load_config(self):
        """Load configuration from file.
        
        Returns:
            dict: Configuration data
        """
        if not self.config_file.exists():
            return {"tracked_files": {}}
            
        with open(self.config_file, "r") as f:
            return json.load(f)

    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)