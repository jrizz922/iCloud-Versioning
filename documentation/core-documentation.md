# iCloud Versioning CLI Documentation

This module provides the command-line interface for the iCloud Versioning tool, built using Click.

## Commands

### `init`

Initialize version tracking for a directory.

```bash
icloud-versioning init DIRECTORY
```

- `DIRECTORY`: Path to the directory to initialize for version tracking

### `status`

Display the status of all tracked files in a directory.

```bash
icloud-versioning status DIRECTORY
```

- `DIRECTORY`: Path to the directory to check status
- Output shows list of tracked files and their current status

### `track`

Start tracking a specific file for versioning.

```bash
icloud-versioning track DIRECTORY FILE
```

- `DIRECTORY`: Path to the directory containing the file
- `FILE`: Path to the file to track

### `restore`

Restore a file to a previous version.

```bash
icloud-versioning restore DIRECTORY FILE --version VERSION
```

- `DIRECTORY`: Path to the directory containing the file
- `FILE`: Path to the file to restore
- `--version`, `-v`: (Optional) Version number to restore to

## Example Usage

```bash
# Initialize a directory
icloud-versioning init ~/Documents/myproject

# Track a file
icloud-versioning track ~/Documents/myproject ~/Documents/myproject/document.txt

# Check status
icloud-versioning status ~/Documents/myproject

# Restore to version 2
icloud-versioning restore ~/Documents/myproject ~/Documents/myproject/document.txt -v 2
```

## Notes

- All directory and file paths must exist
- Version tracking information is managed by the `VersionManager` class
- Commands will provide feedback about the operations performed

## Class: VersionManager

### Overview

The `VersionManager` class handles version tracking for files in a specified directory, maintaining version history and file states.

### Initialization

```python
manager = VersionManager(directory)
```

- `directory`: Path to the directory to manage
- Creates a `.versions` subdirectory for storing version data
- Uses `config.json` to track file metadata

### Methods

#### `initialize()`

Initializes version tracking in the directory.

- Creates `.versions` directory if it doesn't exist
- Initializes configuration file with timestamp

#### `track_file(file_path)`

Starts tracking a file or creates a new version.

- `file_path`: Path to the file to track
- Creates version entry with:
  - Version number
  - File hash
  - Timestamp
  - File size
- Stores a copy of the file in the versions directory

#### `get_status()`

Returns the status of all tracked files.

```python
{
    'file_path': {
        'status': 'unchanged' | 'modified' | 'missing'
    }
}
```

#### `restore_file(file_path, version=None)`

Restores a file to a previous version.

- `file_path`: Path to the file to restore
- `version`: Optional version number (defaults to latest)
- Automatically backs up current version if modified
- Raises exceptions for:
  - Untracked files
  - Invalid version numbers
  - Missing version files

### Internal Methods

#### `_hash_file(file_path)`

Calculates SHA-256 hash of a file.

- Uses 4KB chunks for memory efficiency
- Returns hexadecimal hash string

#### `_load_config()`

Loads configuration from `config.json`.

- Returns empty configuration if file doesn't exist

#### `_save_config()`

Saves current configuration to `config.json`.

- Uses pretty printing with 2-space indentation

### File Structure

```plaintext
tracked_directory/
├── .versions/
│   ├── config.json
│   └── file_name_1/
│       ├── v1
│       ├── v2
│       └── v3
└── tracked_files...
```

### Configuration Format

```json
{
  "tracked_files": {
    "relative/path/to/file": {
      "versions": [
        {
          "version": 1,
          "hash": "sha256_hash",
          "timestamp": "iso_timestamp",
          "size": file_size
        }
      ],
      "added_at": "iso_timestamp"
    }
  },
  "initialized_at": "iso_timestamp"
}
```
