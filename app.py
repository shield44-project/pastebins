"""
Code Storage Website - Main Application
A Flask web application for storing, viewing, categorizing and executing code files
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import subprocess
import tempfile
import json
import re
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['CODES_DIRECTORY'] = 'stored_codes'

# Ensure the codes directory exists
os.makedirs(app.config['CODES_DIRECTORY'], exist_ok=True)

# Supported languages and their configurations
LANGUAGES = {
    'python': {
        'extension': '.py',
        'executor': 'python3',
        'compile': False,
        'type': 'code'
    },
    'java': {
        'extension': '.java',
        'executor': 'java',
        'compile': True,
        'compiler': 'javac',
        'type': 'code'
    },
    'c': {
        'extension': '.c',
        'executor': './program',
        'compile': True,
        'compiler': 'gcc',
        'compiler_flags': ['-o', 'program'],
        'type': 'code'
    },
    'cpp': {
        'extension': '.cpp',
        'executor': './program',
        'compile': True,
        'compiler': 'g++',
        'compiler_flags': ['-o', 'program'],
        'type': 'code'
    },
    'html': {
        'extension': '.html',
        'type': 'web'
    }
}

def get_code_metadata_path(language):
    """Get path to metadata file for a language"""
    # Validate language to prevent path injection
    if language not in LANGUAGES:
        raise ValueError(f"Invalid language: {language}")
    return os.path.join(app.config['CODES_DIRECTORY'], f'{language}_metadata.json')

def load_code_metadata(language):
    """Load metadata for codes in a specific language"""
    # Validate language parameter
    if language not in LANGUAGES:
        return []
    metadata_path = get_code_metadata_path(language)
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return []

def save_code_metadata(language, metadata):
    """Save metadata for codes in a specific language"""
    # Validate language parameter
    if language not in LANGUAGES:
        raise ValueError(f"Invalid language: {language}")
    metadata_path = get_code_metadata_path(language)
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

@app.route('/')
def index():
    """Home page showing all language categories"""
    categories = {}
    for lang in LANGUAGES:
        metadata = load_code_metadata(lang)
        categories[lang] = len(metadata)
    return render_template('index.html', categories=categories, languages=LANGUAGES)

@app.route('/category/<language>')
def category(language):
    """Show all codes for a specific language"""
    if language not in LANGUAGES:
        return "Invalid language", 404
    
    metadata = load_code_metadata(language)
    return render_template('category.html', language=language, codes=metadata)

@app.route('/code/<language>/<int:code_id>')
def view_code(language, code_id):
    """View a specific code file"""
    if language not in LANGUAGES:
        return "Invalid language", 404
    
    metadata = load_code_metadata(language)
    if code_id >= len(metadata):
        return "Code not found", 404
    
    code_info = metadata[code_id]
    code_path = os.path.join(app.config['CODES_DIRECTORY'], language, code_info['filename'])
    
    with open(code_path, 'r') as f:
        code_content = f.read()
    
    # For HTML files, use a different template
    if language == 'html':
        return render_template('view_html.html', 
                             language=language, 
                             code_id=code_id,
                             code_info=code_info, 
                             code_content=code_content)
    
    return render_template('view_code.html', 
                         language=language, 
                         code_id=code_id,
                         code_info=code_info, 
                         code_content=code_content)

@app.route('/upload', methods=['GET', 'POST'])
def upload_code():
    """Upload a new code file"""
    if request.method == 'POST':
        language = request.form.get('language')
        title = request.form.get('title')
        description = request.form.get('description', '')
        code_content = request.form.get('code')
        
        if not language or language not in LANGUAGES:
            return jsonify({'error': 'Invalid language'}), 400
        
        if not title or not code_content:
            return jsonify({'error': 'Title and code are required'}), 400
        
        # Create language directory if it doesn't exist
        lang_dir = os.path.join(app.config['CODES_DIRECTORY'], language)
        os.makedirs(lang_dir, exist_ok=True)
        
        # Load existing metadata
        metadata = load_code_metadata(language)
        
        # Create filename based on title and extension
        filename = f"{title.replace(' ', '_')}{LANGUAGES[language]['extension']}"
        filepath = os.path.join(lang_dir, filename)
        
        # Save the code file
        with open(filepath, 'w') as f:
            f.write(code_content)
        
        # Add to metadata
        code_info = {
            'title': title,
            'description': description,
            'filename': filename,
            'created_at': datetime.now().isoformat()
        }
        metadata.append(code_info)
        save_code_metadata(language, metadata)
        
        return redirect(url_for('category', language=language))
    
    return render_template('upload.html', languages=LANGUAGES)

@app.route('/render/<language>/<int:code_id>')
def render_html(language, code_id):
    """Render HTML file content for iframe display"""
    if language != 'html':
        return "Invalid language for rendering", 404
    
    metadata = load_code_metadata(language)
    if code_id >= len(metadata):
        return "Code not found", 404
    
    code_info = metadata[code_id]
    code_path = os.path.join(app.config['CODES_DIRECTORY'], language, code_info['filename'])
    
    with open(code_path, 'r') as f:
        html_content = f.read()
    
    # Return raw HTML content to be displayed in iframe
    return html_content

@app.route('/execute/<language>/<int:code_id>', methods=['POST'])
def execute_code(language, code_id):
    """Execute a code file and return output"""
    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 400
    
    # HTML files don't need execution
    if language == 'html':
        return jsonify({'error': 'HTML files are rendered, not executed'}), 400
    
    metadata = load_code_metadata(language)
    if code_id >= len(metadata):
        return jsonify({'error': 'Code not found'}), 404
    
    code_info = metadata[code_id]
    code_path = os.path.join(app.config['CODES_DIRECTORY'], language, code_info['filename'])
    
    # Get custom input if provided
    custom_input = request.json.get('input', '') if request.is_json else ''
    
    try:
        output = execute_code_file(language, code_path, custom_input)
        return jsonify({'output': output, 'success': True})
    except Exception:
        # Don't expose detailed error messages to users for security
        return jsonify({'error': 'An error occurred while executing the code', 'success': False}), 500

def execute_code_file(language, code_path, stdin_input=''):
    """Execute a code file and return output"""
    # Validate language
    if language not in LANGUAGES:
        return "Error: Invalid language"
    
    lang_config = LANGUAGES[language]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy file to temp directory
        filename = os.path.basename(code_path)
        
        # Validate filename to prevent command injection
        # Only allow alphanumeric, underscore, dash, and appropriate extension
        import re
        if not re.match(r'^[\w\-]+\.(py|java|c|cpp)$', filename):
            return "Error: Invalid filename"
        
        temp_file = os.path.join(tmpdir, filename)
        
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        with open(temp_file, 'w') as f:
            f.write(code_content)
        
        try:
            # Compile if needed
            if lang_config['compile']:
                if language == 'java':
                    # Java compilation - using list form prevents shell injection
                    compile_cmd = [lang_config['compiler'], filename]
                    compile_result = subprocess.run(
                        compile_cmd,
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=False  # Explicitly set shell=False for security
                    )
                    
                    if compile_result.returncode != 0:
                        return f"Compilation Error:\n{compile_result.stderr}"
                    
                    # For Java, we need to run with class name (without extension)
                    class_name = filename[:-5]  # Remove .java
                    # Validate class name
                    if not re.match(r'^[\w]+$', class_name):
                        return "Error: Invalid class name"
                    execute_cmd = [lang_config['executor'], class_name]
                else:
                    # C/C++ compilation - using list form prevents shell injection
                    compile_cmd = [lang_config['compiler']] + lang_config['compiler_flags'] + [filename]
                    compile_result = subprocess.run(
                        compile_cmd,
                        cwd=tmpdir,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=False  # Explicitly set shell=False for security
                    )
                    
                    if compile_result.returncode != 0:
                        return f"Compilation Error:\n{compile_result.stderr}"
                    
                    execute_cmd = [lang_config['executor']]
            else:
                # Python - direct execution using list form
                execute_cmd = [lang_config['executor'], filename]
            
            # Execute the code - using list form and shell=False for security
            result = subprocess.run(
                execute_cmd,
                cwd=tmpdir,
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=5,
                shell=False  # Explicitly set shell=False for security
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\nErrors/Warnings:\n{result.stderr}"
            
            return output
            
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out (5 seconds limit)"
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    # WARNING: debug=True is for development only. 
    # Set debug=False in production to prevent security vulnerabilities
    # Use environment variable to control debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
