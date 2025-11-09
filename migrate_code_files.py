#!/usr/bin/env python3
"""
Migration script to load existing code files from templates/organized/ 
into the app's storage system (stored_codes/).
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# Define source and destination directories
SOURCE_DIR = 'templates/code_samples'
DEST_DIR = 'stored_codes'

# Language mappings
LANGUAGES = {
    'python': '.py',
    'c': '.c',
    'cpp': '.cpp',
    'html': '.html'
}

def create_storage_structure():
    """Create the stored_codes directory structure."""
    os.makedirs(DEST_DIR, exist_ok=True)
    for lang in LANGUAGES.keys():
        lang_dir = os.path.join(DEST_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        print(f"Created directory: {lang_dir}")

def generate_title_from_filename(filename):
    """Generate a readable title from filename."""
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Replace underscores with spaces and title case
    title = name.replace('_', ' ').replace('-', ' ')
    # Capitalize each word
    title = ' '.join(word.capitalize() for word in title.split())
    return title

def migrate_language_files(language, extension):
    """Migrate all files for a specific language."""
    source_lang_dir = os.path.join(SOURCE_DIR, language)
    dest_lang_dir = os.path.join(DEST_DIR, language)
    
    if not os.path.exists(source_lang_dir):
        print(f"Warning: Source directory not found: {source_lang_dir}")
        return []
    
    # Get all files with the correct extension
    files = [f for f in os.listdir(source_lang_dir) 
             if f.endswith(extension) and os.path.isfile(os.path.join(source_lang_dir, f))]
    
    metadata = []
    
    for filename in sorted(files):
        source_file = os.path.join(source_lang_dir, filename)
        dest_file = os.path.join(dest_lang_dir, filename)
        
        # Copy file
        shutil.copy2(source_file, dest_file)
        
        # Generate metadata
        title = generate_title_from_filename(filename)
        file_stat = os.stat(source_file)
        created_at = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        
        metadata_entry = {
            'title': title,
            'description': f'Migrated from templates/code_samples/{language}/{filename}',
            'filename': filename,
            'created_at': created_at
        }
        metadata.append(metadata_entry)
        
        print(f"  Migrated: {filename} -> {title}")
    
    return metadata

def save_metadata(language, metadata):
    """Save metadata JSON file for a language."""
    metadata_file = os.path.join(DEST_DIR, f'{language}_metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata: {metadata_file} ({len(metadata)} files)")

def main():
    """Main migration function."""
    print("="*60)
    print("Code Files Migration Script")
    print("="*60)
    print()
    
    # Create directory structure
    print("Step 1: Creating storage structure...")
    create_storage_structure()
    print()
    
    # Migrate files for each language
    print("Step 2: Migrating files...")
    for language, extension in LANGUAGES.items():
        print(f"\nMigrating {language.upper()} files...")
        metadata = migrate_language_files(language, extension)
        if metadata:
            save_metadata(language, metadata)
        else:
            print(f"  No files found for {language}")
    
    print()
    print("="*60)
    print("Migration completed successfully!")
    print("="*60)
    print()
    print("Summary:")
    for language in LANGUAGES.keys():
        metadata_file = os.path.join(DEST_DIR, f'{language}_metadata.json')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                count = len(json.load(f))
            print(f"  {language.upper()}: {count} files")
    print()

if __name__ == '__main__':
    main()
