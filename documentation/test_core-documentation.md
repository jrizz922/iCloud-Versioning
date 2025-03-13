# iCloud Versioning Core Tests Documentation

This module contains tests for the core functionality of the iCloud Versioning system, specifically for the `VersionManager` class.

## Fixtures

### `temp_dir`

Creates a temporary directory for testing purposes.

- Yields the path to the temporary directory
- Cleans up the directory after the test

### `test_file`

Creates a test file within the temporary directory.

- Depends on `temp_dir` fixture
- Yields the path to the test file

## Test Functions

### `test_initialize(temp_dir)`

Tests the initialization of version tracking.

- Creates an instance of `VersionManager` with `temp_dir`
- Calls `initialize()` method
- Asserts that the `.versions` directory and `config.json` file are created

### `test_track_file(temp_dir, test_file)`

Tests tracking a file.

- Creates an instance of `VersionManager` with `temp_dir`
- Calls `initialize()` method
- Calls `track_file(test_file)` method
- Asserts that the file is added to the `tracked_files` in the configuration
- Asserts that the file has one version entry

### `test_get_status(temp_dir, test_file)`

Tests getting the status of tracked files.

- Creates an instance of `VersionManager` with `temp_dir`
- Calls `initialize()` method
- Calls `track_file(test_file)` method
- Calls `get_status()` method
- Asserts that the file status is `unchanged`
- Modifies the file content
- Calls `get_status()` method again
- Asserts that the file status is `modified`

### `test_restore_file(temp_dir, test_file)`

Tests restoring a file to a previous version.

- Creates an instance of `VersionManager` with `temp_dir`
- Calls `initialize()` method
- Calls `track_file(test_file)` method
- Modifies the file content
- Calls `track_file(test_file)` method again to track the modified version
- Calls `restore_file(test_file, 1)` method to restore to the first version
- Asserts that the file content matches the initial content

## Example Usage

To run the tests, use the following command:

```bash
pytest tests/test_core.py
```

This will execute all the test functions and provide feedback on their success or failure.