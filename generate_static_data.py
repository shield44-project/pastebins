#!/usr/bin/env python3
"""
Generate JavaScript data file from stored_codes for static site deployment.
This allows the static site on Netlify to access the pre-loaded code files.
"""

import os
import json
from pathlib import Path

STORED_CODES_DIR = 'stored_codes'
OUTPUT_JS_FILE = 'static/preloaded_codes.js'
LANGUAGES = ['python', 'c', 'cpp', 'html']

def load_code_file(language, filename):
    """Load code file content."""
    file_path = os.path.join(STORED_CODES_DIR, language, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load {file_path}: {e}")
        return ""

def generate_static_data():
    """Generate JavaScript file with all code files embedded."""
    all_files = []
    
    for lang in LANGUAGES:
        # Load metadata
        metadata_file = os.path.join(STORED_CODES_DIR, f'{lang}_metadata.json')
        if not os.path.exists(metadata_file):
            print(f"Skipping {lang}: metadata not found")
            continue
            
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Load each code file
        for idx, code_info in enumerate(metadata):
            filename = code_info['filename']
            content = load_code_file(lang, filename)
            
            file_entry = {
                'id': f"{lang}_{idx}",
                'language': lang,
                'title': code_info['title'],
                'description': code_info.get('description', ''),
                'filename': filename,
                'code': content,
                'created': code_info['created_at']
            }
            all_files.append(file_entry)
    
    # Generate JavaScript file
    os.makedirs(os.path.dirname(OUTPUT_JS_FILE), exist_ok=True)
    
    with open(OUTPUT_JS_FILE, 'w', encoding='utf-8') as f:
        f.write('// Auto-generated file with pre-loaded code files\n')
        f.write('// Generated from stored_codes/ directory\n\n')
        f.write('const PRELOADED_CODES = ')
        f.write(json.dumps(all_files, indent=2, ensure_ascii=False))
        f.write(';\n\n')
        f.write('// Function to load preloaded codes into localStorage\n')
        f.write('function loadPreloadedCodes() {\n')
        f.write('    const STORAGE_KEY = "pastebin_codes";\n')
        f.write('    \n')
        f.write('    // Always load preloaded codes (overwrite on each page load)\n')
        f.write('    // This ensures the static site always has the latest files\n')
        f.write('    localStorage.setItem(STORAGE_KEY, JSON.stringify(PRELOADED_CODES));\n')
        f.write('    \n')
        f.write('    console.log(`Loaded ${PRELOADED_CODES.length} preloaded code files`);\n')
        f.write('    \n')
        f.write('    // Dispatch custom event to notify that codes are loaded\n')
        f.write('    if (typeof window !== "undefined") {\n')
        f.write('        window.dispatchEvent(new CustomEvent("preloadedCodesReady"));\n')
        f.write('    }\n')
        f.write('}\n\n')
        f.write('// Auto-load immediately (before DOMContentLoaded)\n')
        f.write('if (typeof window !== "undefined") {\n')
        f.write('    loadPreloadedCodes();\n')
        f.write('}\n')
    
    print(f"\n✅ Generated {OUTPUT_JS_FILE} with {len(all_files)} code files")
    print(f"\nFile sizes by language:")
    lang_counts = {}
    for file in all_files:
        lang = file['language']
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    for lang, count in sorted(lang_counts.items()):
        print(f"  {lang.upper()}: {count} files")
    
    return OUTPUT_JS_FILE

if __name__ == '__main__':
    generate_static_data()
