# Migration Guide

This document explains the migration of code files from `templates/organized/` to `stored_codes/`.

## What Was Done

### 1. Migration Script
A Python script (`migrate_code_files.py`) was created to:
- Copy all code files from `templates/organized/` to `stored_codes/`
- Generate metadata JSON files for each programming language
- Create proper directory structure for the application

### 2. Files Migrated
- **Python**: 50 files
- **C**: 32 files
- **C++**: 6 files
- **HTML**: 7 files
- **Total**: 95 files

### 3. Directory Structure
```
stored_codes/
├── python/
│   ├── *.py files
│   └── ...
├── c/
│   ├── *.c files
│   └── ...
├── cpp/
│   ├── *.cpp files
│   └── ...
├── html/
│   ├── *.html files
│   └── ...
├── python_metadata.json
├── c_metadata.json
├── cpp_metadata.json
└── html_metadata.json
```

## Running the Migration

If you need to re-run the migration (e.g., after adding new files to `templates/code_samples/`):

```bash
python3 migrate_code_files.py
```

**Note**: This will overwrite existing files and metadata in `stored_codes/`.

## Metadata Format

Each `<language>_metadata.json` file contains an array of objects with this structure:

```json
[
  {
    "title": "Human Readable Title",
    "description": "Description of the file",
    "filename": "actual_filename.ext",
    "created_at": "2025-11-09T13:03:00.000000"
  }
]
```

## Post-Migration

After migration:
1. All files are accessible through the web interface
2. Files can be viewed with syntax highlighting
3. Code can be executed directly from the browser
4. Files are searchable and filterable on the "All Files" page

## Important Notes

- The `stored_codes/` directory is in `.gitignore` and should not be committed
- Original files remain in `templates/code_samples/` as reference/backup
- To add new code to the application, use the web upload interface or manually add files to `stored_codes/` with appropriate metadata
