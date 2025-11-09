"""
Code Storage Website - Main Application
A Flask web application for storing, viewing, categorizing and executing code files
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
import subprocess
import tempfile
import json
import re
import base64
import hmac
import hashlib
import time
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['CODES_DIRECTORY'] = 'stored_codes'
app.config['ENCRYPTED_DIRECTORY'] = 'encrypted'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Load private key for decryption (if available)
PRIVATE_KEY = None
ENCRYPTION_SECRET = os.environ.get('TOKEN_SECRET', 'dev-secret-change-in-production')

def load_private_key():
    """Load RSA private key from file if it exists."""
    private_key_path = 'private_key.pem'
    if os.path.exists(private_key_path):
        try:
            with open(private_key_path, 'rb') as f:
                return serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
        except Exception as e:
            print(f"Warning: Could not load private key: {e}")
    return None

PRIVATE_KEY = load_private_key()

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
    'javascript': {
        'extension': '.js',
        'executor': 'node',
        'compile': False,
        'type': 'code'
    },
    'typescript': {
        'extension': '.ts',
        'executor': 'ts-node',
        'compile': False,
        'type': 'code'
    },
    'react': {
        'extension': '.jsx',
        'type': 'web'
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

# Encryption/Decryption functions
def load_encrypted_manifest():
    """Load manifest of encrypted files."""
    manifest_path = Path(app.config['ENCRYPTED_DIRECTORY']) / 'manifest.json'
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            return json.load(f)
    return {}

def decrypt_file_content(encrypted_data, private_key):
    """
    Decrypt file using hybrid RSA+AES scheme.
    encrypted_data should have: encrypted_key, nonce, ciphertext (all base64).
    Returns plaintext bytes.
    """
    # Decode from base64
    encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
    nonce = base64.b64decode(encrypted_data['nonce'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    
    # Decrypt AES key with RSA private key
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Decrypt file content with AES-GCM
    cipher = AESGCM(aes_key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    
    return plaintext

def generate_token(filename, ttl=3600):
    """Generate HMAC token for file access."""
    expiry = int(time.time()) + ttl
    message = f"{filename}:{expiry}"
    signature = hmac.new(
        ENCRYPTION_SECRET.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    token_data = f"{message}:{signature}"
    return base64.urlsafe_b64encode(token_data.encode('utf-8')).decode('utf-8')

def verify_token(token, filename):
    """Verify HMAC token and check expiry."""
    try:
        token_data = base64.urlsafe_b64decode(token).decode('utf-8')
        parts = token_data.rsplit(':', 1)
        if len(parts) != 2:
            return False
        
        message, signature = parts
        msg_parts = message.split(':', 1)
        if len(msg_parts) != 2:
            return False
        
        token_filename, expiry_str = msg_parts
        
        if token_filename != filename:
            return False
        
        expiry = int(expiry_str)
        if time.time() > expiry:
            return False
        
        expected_sig = hmac.new(
            ENCRYPTION_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_sig)
    except Exception:
        return False

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
    
    # Check language type
    lang_config = LANGUAGES[language]
    
    # For HTML files, use a different template
    if language == 'html':
        return render_template('view_html.html', 
                             language=language, 
                             code_id=code_id,
                             code_info=code_info, 
                             code_content=code_content)
    
    # For React/JSX files, use HTML viewer since they need to be rendered
    if language == 'react':
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
        
        # Validate title to prevent path traversal
        if '/' in title or '\\' in title or title.startswith('.'):
            return jsonify({'error': 'Invalid title - cannot contain path separators'}), 400
        
        # Create language directory if it doesn't exist
        lang_dir = os.path.join(app.config['CODES_DIRECTORY'], language)
        os.makedirs(lang_dir, exist_ok=True)
        
        # Load existing metadata
        metadata = load_code_metadata(language)
        
        # Create filename based on title and extension - sanitize for filesystem
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        if not safe_title:
            safe_title = 'unnamed'
        filename = f"{safe_title}{LANGUAGES[language]['extension']}"
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

@app.route('/upload-files', methods=['POST'])
def upload_files():
    """Upload multiple code files"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    language = request.form.get('language')
    
    if not language or language not in LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 400
    
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'No files selected'}), 400
    
    # Create language directory if it doesn't exist
    lang_dir = os.path.join(app.config['CODES_DIRECTORY'], language)
    os.makedirs(lang_dir, exist_ok=True)
    
    # Load existing metadata
    metadata = load_code_metadata(language)
    
    uploaded_count = 0
    for file in files:
        if file and file.filename:
            # Secure the filename
            filename = file.filename
            # Basic validation of filename
            if not re.match(r'^[\w\-\.]+$', filename):
                continue  # Skip invalid filenames
            
            # Check file extension matches language
            expected_ext = LANGUAGES[language]['extension']
            if not filename.endswith(expected_ext):
                continue  # Skip files with wrong extension
            
            # Save the file
            filepath = os.path.join(lang_dir, filename)
            file.save(filepath)
            
            # Add to metadata
            title = filename.rsplit('.', 1)[0].replace('_', ' ').title()
            code_info = {
                'title': title,
                'description': f'Uploaded from file: {filename}',
                'filename': filename,
                'created_at': datetime.now().isoformat()
            }
            metadata.append(code_info)
            uploaded_count += 1
    
    # Save updated metadata
    save_code_metadata(language, metadata)
    
    if uploaded_count == 0:
        return jsonify({'error': 'No valid files were uploaded'}), 400
    
    return redirect(url_for('category', language=language))

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
    
    # HTML and React files don't need execution
    lang_config = LANGUAGES[language]
    if lang_config.get('type') == 'web' and language not in ['javascript', 'typescript']:
        return jsonify({'error': 'This file type is rendered, not executed'}), 400
    
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
    
    # Check if execution is supported
    if lang_config.get('type') == 'web' and language != 'javascript':
        return "Error: This language type is for web preview only"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy file to temp directory
        filename = os.path.basename(code_path)
        
        # Validate filename to prevent command injection
        # Only allow alphanumeric, underscore, dash, and appropriate extension
        import re
        if not re.match(r'^[\w\-]+\.(py|java|c|cpp|js|ts)$', filename):
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
                elif language == 'typescript':
                    # TypeScript requires ts-node
                    execute_cmd = [lang_config['executor'], filename]
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
                # Python/JavaScript - direct execution using list form
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

# Encrypted Files Routes
@app.route('/encrypted-viewer')
def encrypted_viewer():
    """Serve the encrypted files viewer page using template."""
    return render_template('encrypted_viewer.html')

@app.route('/encrypted/manifest')
def encrypted_manifest():
    """Serve encrypted files manifest."""
    manifest = load_encrypted_manifest()
    return jsonify(manifest)

@app.route('/encrypted/file')
def serve_encrypted_file():
    """
    Serve decrypted file if valid token provided.
    Query params: name=<filename>, token=<token>
    """
    if not PRIVATE_KEY:
        return jsonify({'error': 'Decryption not available (private key not found)'}), 503
    
    filename = request.args.get('name')
    token = request.args.get('token')
    
    if not filename or not token:
        return jsonify({'error': 'Missing name or token parameter'}), 400
    
    # Verify token
    if not verify_token(token, filename):
        return jsonify({'error': 'Invalid or expired token'}), 403
    
    # Validate filename to prevent path traversal
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # Load encrypted file
    enc_filename = f"{filename}.enc.json"
    enc_path = Path(app.config['ENCRYPTED_DIRECTORY']) / enc_filename
    
    # Verify the path is within the encrypted directory (prevent path traversal)
    try:
        enc_path = enc_path.resolve()
        encrypted_dir = Path(app.config['ENCRYPTED_DIRECTORY']).resolve()
        if not str(enc_path).startswith(str(encrypted_dir)):
            return jsonify({'error': 'Invalid file path'}), 400
    except Exception:
        return jsonify({'error': 'Invalid file path'}), 400
    
    if not enc_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    try:
        with open(enc_path, 'r') as f:
            encrypted_data = json.load(f)
        
        # Decrypt file
        plaintext = decrypt_file_content(
            encrypted_data['payload'],
            PRIVATE_KEY
        )
        
        # Return plaintext
        return plaintext, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    except Exception as e:
        print(f"Decryption error: {e}")
        return jsonify({'error': 'Decryption failed'}), 500

@app.route('/encrypted/token/<filename>')
def get_file_token(filename):
    """Generate a token for accessing an encrypted file."""
    # In production, add authentication here
    ttl = int(request.args.get('ttl', 3600))
    token = generate_token(filename, ttl)
    return jsonify({'token': token, 'filename': filename, 'expires_in': ttl})

@app.route('/encrypted/list')
def list_encrypted_files():
    """List all encrypted files with their tokens."""
    manifest = load_encrypted_manifest()
    files = []
    for orig_name in manifest.keys():
        token = generate_token(orig_name, 3600)  # 1 hour token
        files.append({
            'name': orig_name,
            'token': token,
            'view_url': f"/encrypted/file?name={orig_name}&token={token}"
        })
    return jsonify({'files': files})

@app.route('/api/folders', methods=['GET'])
def list_folders():
    """List all language folders and their file counts."""
    folders = []
    for language, config in LANGUAGES.items():
        folder_path = os.path.join(app.config['CODES_DIRECTORY'], language)
        if os.path.exists(folder_path):
            file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        else:
            file_count = 0
        
        folders.append({
            'language': language,
            'extension': config.get('extension', ''),
            'file_count': file_count,
            'type': config.get('type', 'code')
        })
    
    return jsonify({'folders': folders})

@app.route('/api/folders/<language>', methods=['POST'])
def create_folder(language):
    """Create a folder for a specific language."""
    # SECURITY: Validate language parameter against whitelist to prevent path injection
    # Only predefined language keys from LANGUAGES dict are allowed
    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 400
    
    # Safe to use language here as it's validated against LANGUAGES whitelist
    # The language value can only be one of: python, java, c, cpp, javascript, typescript, react, html
    folder_path = os.path.join(app.config['CODES_DIRECTORY'], language)
    
    # Create folder if it doesn't exist
    try:
        os.makedirs(folder_path, exist_ok=True)
        return jsonify({
            'success': True,
            'message': f'Folder created for {language}'
            # Don't expose internal path to user
        })
    except OSError as e:
        # Log the error but don't expose stack trace to user
        app.logger.error(f'Failed to create folder for {language}: {e}')
        return jsonify({'error': 'Failed to create folder'}), 500

if __name__ == '__main__':
    # WARNING: debug=True is for development only. 
    # Set debug=False in production to prevent security vulnerabilities
    # Use environment variable to control debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
