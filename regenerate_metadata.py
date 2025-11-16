#!/usr/bin/env python3
"""
Script to regenerate metadata for all stored code files.
This will scan the stored_codes directory and create metadata entries for all files.
"""

import os
import json
from datetime import datetime

# Language configurations
LANGUAGES = {
    'python': {'extension': '.py'},
    'java': {'extension': '.java'},
    'c': {'extension': '.c'},
    'cpp': {'extension': '.cpp'},
    'javascript': {'extension': '.js'},
    'typescript': {'extension': '.ts'},
    'react': {'extension': '.jsx'},
    'html': {'extension': '.html'}
}

CODES_DIRECTORY = 'stored_codes'

def regenerate_metadata_for_language(language):
    """Regenerate metadata for a specific language."""
    print(f"\nProcessing {language}...")
    
    lang_dir = os.path.join(CODES_DIRECTORY, language)
    if not os.path.exists(lang_dir):
        print(f"  Directory not found: {lang_dir}")
        return
    
    extension = LANGUAGES[language]['extension']
    
    # Find all files with the language extension
    files = [f for f in os.listdir(lang_dir) if f.endswith(extension)]
    
    if not files:
        print(f"  No {extension} files found")
        return
    
    print(f"  Found {len(files)} files")
    
    # Load existing metadata
    metadata_path = os.path.join(CODES_DIRECTORY, f'{language}_metadata.json')
    existing_metadata = []
    existing_filenames = set()
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            existing_metadata = json.load(f)
            existing_filenames = {m['filename'] for m in existing_metadata}
        print(f"  Existing metadata entries: {len(existing_metadata)}")
    
    # Add metadata for new files
    new_count = 0
    for filename in sorted(files):
        if filename not in existing_filenames:
            # Create a title from filename
            title = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
            
            # Get file creation time or use current time
            file_path = os.path.join(lang_dir, filename)
            try:
                file_time = os.path.getmtime(file_path)
                created_at = datetime.fromtimestamp(file_time).isoformat()
            except:
                created_at = datetime.now().isoformat()
            
            metadata_entry = {
                'title': title,
                'description': f'Code file: {filename}',
                'filename': filename,
                'created_at': created_at,
                'encrypted': False,
                'is_secret': False
            }
            
            existing_metadata.append(metadata_entry)
            new_count += 1
    
    # Save updated metadata
    with open(metadata_path, 'w') as f:
        json.dump(existing_metadata, f, indent=2)
    
    print(f"  ✓ Added {new_count} new entries")
    print(f"  ✓ Total metadata entries: {len(existing_metadata)}")

def main():
    """Regenerate metadata for all languages."""
    print("=" * 70)
    print("Regenerating Metadata for All Languages")
    print("=" * 70)
    
    if not os.path.exists(CODES_DIRECTORY):
        print(f"Error: {CODES_DIRECTORY} directory not found")
        return 1
    
    for language in LANGUAGES:
        regenerate_metadata_for_language(language)
    
    print("\n" + "=" * 70)
    print("Metadata regeneration complete!")
    print("=" * 70)
    print()
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
