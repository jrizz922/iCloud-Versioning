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
