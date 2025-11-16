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
import shutil
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# GitHub integration
try:
    from github import Github, GithubException
    GITHUB_ENABLED = True
except ImportError:
    GITHUB_ENABLED = False
    app.logger.warning("PyGithub not installed. GitHub integration disabled.")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['CODES_DIRECTORY'] = os.environ.get('CODES_DIRECTORY', 'stored_codes')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# GitHub configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'shield44-project/pastebins')
GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH', 'main')

# Password-based encryption utilities
def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits for AES-256
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_content_with_password(content: str, password: str) -> dict:
    """
    Encrypt content with password-based encryption.
    Returns dict with salt, nonce, and ciphertext (all base64 encoded).
    """
    # Generate random salt and nonce
    salt = os.urandom(16)  # 128 bits
    nonce = os.urandom(12)  # 96 bits for AES-GCM
    
    # Derive key from password
    key = derive_key_from_password(password, salt)
    
    # Encrypt content
    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, content.encode('utf-8'), None)
    
    return {
        'salt': base64.b64encode(salt).decode('utf-8'),
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
    }

def decrypt_content_with_password(encrypted_data: dict, password: str) -> str:
    """
    Decrypt content with password.
    Returns decrypted string or raises exception on failure.
    """
    # Decode from base64
    salt = base64.b64decode(encrypted_data['salt'])
    nonce = base64.b64decode(encrypted_data['nonce'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    
    # Derive key from password
    key = derive_key_from_password(password, salt)
    
    # Decrypt content
    cipher = AESGCM(key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    
    return plaintext.decode('utf-8')

# GitHub Integration Functions
def commit_file_to_github(file_path, file_content, commit_message):
    """
    Commit a file to GitHub repository.
    Returns True if successful, False otherwise.
    """
    if not GITHUB_ENABLED or not GITHUB_TOKEN:
        app.logger.warning("GitHub integration not configured. Skipping commit.")
        return False
    
    try:
        # Initialize GitHub client
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        
        # Try to get existing file
        try:
            contents = repo.get_contents(file_path, ref=GITHUB_BRANCH)
            # File exists, update it
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                sha=contents.sha,
                branch=GITHUB_BRANCH
            )
            app.logger.info(f"Updated file in GitHub: {file_path}")
        except GithubException as e:
            if e.status == 404:
                # File doesn't exist, create it
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=file_content,
                    branch=GITHUB_BRANCH
                )
                app.logger.info(f"Created file in GitHub: {file_path}")
            else:
                raise
        
        return True
        
    except Exception as e:
        app.logger.error(f"Failed to commit to GitHub: {str(e)}")
        return False

def commit_metadata_to_github(language, metadata):
    """
    Commit metadata file to GitHub repository.
    Returns True if successful, False otherwise.
    """
    metadata_path = f"stored_codes/{language}_metadata.json"
    metadata_content = json.dumps(metadata, indent=2)
    commit_message = f"Update {language} metadata via web upload"
    
    return commit_file_to_github(metadata_path, metadata_content, commit_message)

def check_compiler_available(compiler):
    """Check if a compiler/interpreter is available in the system."""
    return shutil.which(compiler) is not None

def execute_code_online(code_content, stdin_input='', language='c'):
    """
    Execute C, C++, or Java code using an online compiler API.
    Uses the Wandbox API (https://wandbox.org/).
    
    Args:
        code_content: The source code to execute
        stdin_input: Input to provide to the program
        language: Programming language ('c', 'cpp', or 'java')
    
    Returns:
        String containing the execution output or error message
    """
    try:
        # Prepare the request to Wandbox API
        url = 'https://wandbox.org/api/compile.json'
        
        # Select compiler based on language
        compiler_map = {
            'c': 'gcc-head',
            'cpp': 'clang-head',  # Use clang for C++ to avoid gcc-head issues
            'java': 'openjdk-head'
        }
        
        compiler_option_map = {
            'c': '-Wall -O2',
            'cpp': '-Wall -O2 -std=c++17',
            'java': ''
        }
        
        language_name_map = {
            'c': 'C',
            'cpp': 'C++',
            'java': 'Java'
        }
        
        compiler = compiler_map.get(language, 'gcc-head')
        compiler_options = compiler_option_map.get(language, '')
        language_display = language_name_map.get(language, language.upper())
        
        # Prepare the payload for Wandbox
        payload = {
            'compiler': compiler,
            'code': code_content,
            'stdin': stdin_input,
            'options': '',
            'compiler-option-raw': compiler_options,
            'runtime-option-raw': '',
            'save': False
        }
        
        # Send the request
        headers = {
            'Content-Type': 'application/json'
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Extract output
            output = ''
            
            # Check for compilation error
            if 'compiler_error' in result and result['compiler_error']:
                output = 'Compilation Error:\n' + result['compiler_error']
                return output
            
            # Check for compilation message (warnings)
            if 'compiler_message' in result and result['compiler_message']:
                output += result['compiler_message'] + '\n'
            
            # Get program output
            if 'program_output' in result and result['program_output']:
                output += result['program_output']
            
            # Check for program error
            if 'program_error' in result and result['program_error']:
                output += '\nErrors:\n' + result['program_error']
            
            # Check for execution status
            if 'status' in result and result['status'] != '0':
                if not output.strip():
                    output = f"Program exited with status {result['status']}"
            
            return output if output.strip() else 'Program executed successfully with no output.'
            
    except urllib.error.URLError as e:
        # Fallback message with helpful instructions
        compiler_install = {
            'c': 'gcc',
            'cpp': 'g++',
            'java': 'Java JDK'
        }
        install_name = compiler_install.get(language, 'the compiler')
        return f"Error: Unable to connect to online compiler service.\nPlease ensure you have an internet connection or install {install_name} locally to compile {language_display} code.\nDetails: {str(e)}"
    except urllib.error.HTTPError as e:
        compiler_install = {
            'c': 'gcc',
            'cpp': 'g++',
            'java': 'Java JDK'
        }
        install_name = compiler_install.get(language, 'the compiler')
        return f"Error: Online compiler service returned an error (HTTP {e.code}).\nPlease try again later or install {install_name} locally."
    except Exception as e:
        return f"Error: Failed to execute code online.\nDetails: {str(e)}"

def execute_c_code_online(code_content, stdin_input=''):
    """
    Execute C code using an online compiler API.
    Uses the Wandbox API (https://wandbox.org/).
    
    This is a wrapper around execute_code_online for backward compatibility.
    """
    return execute_code_online(code_content, stdin_input, 'c')

def execute_cpp_code_online(code_content, stdin_input=''):
    """
    Execute C++ code using an online compiler API.
    Uses the Wandbox API (https://wandbox.org/).
    """
    return execute_code_online(code_content, stdin_input, 'cpp')

def execute_java_code_online(code_content, stdin_input=''):
    """
    Execute Java code using an online compiler API.
    Uses the Wandbox API (https://wandbox.org/).
    """
    return execute_code_online(code_content, stdin_input, 'java')

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

@app.route('/')
def index():
    """Home page showing all language categories"""
    categories = {}
    for lang in LANGUAGES:
        metadata = load_code_metadata(lang)
        categories[lang] = len(metadata)
    return render_template('index.html', categories=categories, languages=LANGUAGES)

@app.route('/all-files')
def all_files():
    """Show all code files from all languages"""
    all_files_list = []
    language_counts = {}
    
    for lang in LANGUAGES:
        metadata = load_code_metadata(lang)
        language_counts[lang] = len(metadata)
        
        for idx, code_info in enumerate(metadata):
            # Skip secret files in all files view
            if code_info.get('is_secret', False):
                continue
                
            file_entry = {
                'id': idx,
                'language': lang,
                'title': code_info['title'],
                'description': code_info.get('description', ''),
                'filename': code_info['filename'],
                'created_at': code_info['created_at'],
                'encrypted': code_info.get('encrypted', False)
            }
            all_files_list.append(file_entry)
    
    # Sort by creation date (newest first)
    all_files_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    total_files = len(all_files_list)
    
    return render_template('all_files.html', 
                         all_files=all_files_list,
                         total_files=total_files,
                         language_counts=language_counts)

@app.route('/secret-folders')
def secret_folders():
    """Show all secret files from all languages"""
    secret_files_list = []
    language_counts = {}
    
    for lang in LANGUAGES:
        metadata = load_code_metadata(lang)
        secret_count = 0
        
        for idx, code_info in enumerate(metadata):
            # Only show secret files
            if not code_info.get('is_secret', False):
                continue
            
            secret_count += 1
            file_entry = {
                'id': idx,
                'language': lang,
                'title': code_info['title'],
                'description': code_info.get('description', ''),
                'filename': code_info['filename'],
                'created_at': code_info['created_at'],
                'encrypted': code_info.get('encrypted', False)
            }
            secret_files_list.append(file_entry)
        
        if secret_count > 0:
            language_counts[lang] = secret_count
    
    # Sort by creation date (newest first)
    secret_files_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    total_files = len(secret_files_list)
    
    return render_template('secret_folders.html', 
                         secret_files=secret_files_list,
                         total_files=total_files,
                         language_counts=language_counts)

@app.route('/category/<language>')
def category(language):
    """Show all codes for a specific language"""
    if language not in LANGUAGES:
        return "Invalid language", 404
    
    show_secret = request.args.get('show_secret', 'false').lower() == 'true'
    
    metadata = load_code_metadata(language)
    
    # Filter out secret files unless show_secret is True
    if not show_secret:
        metadata = [code for code in metadata if not code.get('is_secret', False)]
    else:
        # Only show secret files when requested
        metadata = [code for code in metadata if code.get('is_secret', False)]
    
    return render_template('category.html', language=language, codes=metadata, show_secret=show_secret)

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
    
    # Check if file is encrypted
    is_encrypted = code_info.get('encrypted', False)
    
    if is_encrypted:
        # For encrypted files, show a password prompt instead of content
        code_content = None
    else:
        # Read normal file content
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

@app.route('/decrypt/<language>/<int:code_id>', methods=['POST'])
def decrypt_code(language, code_id):
    """Decrypt an encrypted code file"""
    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 404
    
    metadata = load_code_metadata(language)
    if code_id >= len(metadata):
        return jsonify({'error': 'Code not found'}), 404
    
    code_info = metadata[code_id]
    
    if not code_info.get('encrypted', False):
        return jsonify({'error': 'This file is not encrypted'}), 400
    
    password = request.json.get('password') if request.is_json else request.form.get('password')
    
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # Load encrypted file
    enc_path = os.path.join(app.config['CODES_DIRECTORY'], language, code_info['filename'] + '.enc')
    
    try:
        with open(enc_path, 'r') as f:
            encrypted_data = json.load(f)
        
        # Decrypt content
        code_content = decrypt_content_with_password(encrypted_data, password)
        
        return jsonify({'success': True, 'content': code_content})
    
    except Exception as e:
        return jsonify({'error': 'Decryption failed. Wrong password or corrupted file.'}), 403

@app.route('/delete/<language>/<int:code_id>', methods=['POST', 'DELETE'])
def delete_code(language, code_id):
    """Delete a code file"""
    if language not in LANGUAGES:
        return jsonify({'error': 'Invalid language'}), 404
    
    metadata = load_code_metadata(language)
    if code_id >= len(metadata):
        return jsonify({'error': 'Code not found'}), 404
    
    code_info = metadata[code_id]
    
    try:
        # Delete the file
        code_path = os.path.join(app.config['CODES_DIRECTORY'], language, code_info['filename'])
        if os.path.exists(code_path):
            os.remove(code_path)
        
        # Delete encrypted file if it exists
        if code_info.get('encrypted', False):
            enc_path = code_path + '.enc'
            if os.path.exists(enc_path):
                os.remove(enc_path)
        
        # Remove from metadata
        metadata.pop(code_id)
        save_code_metadata(language, metadata)
        
        # Commit to GitHub if configured
        if GITHUB_ENABLED and GITHUB_TOKEN:
            try:
                commit_metadata_to_github(language, metadata)
                app.logger.info(f"Deleted file from GitHub: {code_info['filename']}")
            except Exception as e:
                app.logger.warning(f"File deleted locally but GitHub sync failed: {str(e)}")
        
        return jsonify({'success': True, 'message': 'Code deleted successfully'})
    
    except Exception as e:
        app.logger.error(f"Failed to delete code: {str(e)}")
        return jsonify({'error': 'Failed to delete code'}), 500

@app.route('/upload', methods=['GET', 'POST'])
def upload_code():
    """Upload a new code file"""
    if request.method == 'POST':
        try:
            language = request.form.get('language')
            title = request.form.get('title')
            description = request.form.get('description', '')
            code_content = request.form.get('code')
            encrypt = request.form.get('encrypt') == 'on'
            password = request.form.get('password', '')
            is_secret = request.form.get('is_secret') == 'on'
            
            if not language or language not in LANGUAGES:
                return jsonify({'error': 'Invalid language'}), 400
            
            if not title or not code_content:
                return jsonify({'error': 'Title and code are required'}), 400
            
            if encrypt and not password:
                return jsonify({'error': 'Password is required for encryption'}), 400
            
            # Validate title to prevent path traversal
            if '/' in title or '\\' in title or title.startswith('.'):
                return jsonify({'error': 'Invalid title - cannot contain path separators'}), 400
            
            # Create language directory if it doesn't exist
            lang_dir = os.path.join(app.config['CODES_DIRECTORY'], language)
            try:
                os.makedirs(lang_dir, exist_ok=True)
            except OSError as e:
                app.logger.error(f"Failed to create directory {lang_dir}: {str(e)}")
                return jsonify({'error': 'Failed to create storage directory. The server may have limited write permissions.'}), 500
            
            # Load existing metadata
            metadata = load_code_metadata(language)
            
            # Create filename based on title and extension - sanitize for filesystem
            safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
            if not safe_title:
                safe_title = 'unnamed'
            filename = f"{safe_title}{LANGUAGES[language]['extension']}"
            filepath = os.path.join(lang_dir, filename)
            
            # Handle encryption if requested
            encrypted_data = None
            try:
                if encrypt:
                    encrypted_data = encrypt_content_with_password(code_content, password)
                    # Save encrypted data to file
                    with open(filepath + '.enc', 'w') as f:
                        json.dump(encrypted_data, f)
                else:
                    # Save the code file normally
                    with open(filepath, 'w') as f:
                        f.write(code_content)
            except PermissionError as e:
                app.logger.error(f"Permission error saving file {filepath}: {str(e)}")
                return jsonify({'error': 'Permission denied - cannot write file. The server may have limited write permissions.'}), 500
            except IOError as e:
                app.logger.error(f"I/O error saving file {filepath}: {str(e)}")
                return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
            
            # Add to metadata
            code_info = {
                'title': title,
                'description': description,
                'filename': filename,
                'created_at': datetime.now().isoformat(),
                'encrypted': encrypt,
                'is_secret': is_secret
            }
            metadata.append(code_info)
            
            try:
                save_code_metadata(language, metadata)
            except Exception as e:
                app.logger.error(f"Failed to save metadata: {str(e)}")
                return jsonify({'error': 'File saved but failed to save metadata. Please try again.'}), 500
            
            # Commit to GitHub if configured
            if GITHUB_ENABLED and GITHUB_TOKEN:
                try:
                    # Commit the code file
                    github_file_path = f"stored_codes/{language}/{filename}"
                    if encrypt:
                        github_file_path += '.enc'
                        file_content_to_commit = json.dumps(encrypted_data, indent=2)
                    else:
                        file_content_to_commit = code_content
                    
                    commit_message = f"Add {language} file: {title} via web upload"
                    commit_file_to_github(github_file_path, file_content_to_commit, commit_message)
                    
                    # Commit the metadata
                    commit_metadata_to_github(language, metadata)
                    
                    app.logger.info(f"Successfully committed to GitHub: {github_file_path}")
                except Exception as e:
                    app.logger.warning(f"File saved locally but GitHub commit failed: {str(e)}")
                    # Don't fail the upload if GitHub commit fails
            
            return redirect(url_for('category', language=language))
        
        except Exception as e:
            app.logger.error(f"Unexpected error in upload_code: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred during code upload. Please try again.'}), 500
    
    return render_template('upload.html', languages=LANGUAGES)

@app.route('/upload-files', methods=['POST'])
def upload_files():
    """Upload multiple code files"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        language = request.form.get('language')
        encrypt = request.form.get('encrypt') == 'on'
        password = request.form.get('password', '')
        is_secret = request.form.get('is_secret') == 'on'
        
        if not language or language not in LANGUAGES:
            return jsonify({'error': 'Invalid language'}), 400
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files selected'}), 400
        
        if encrypt and not password:
            return jsonify({'error': 'Password is required for encryption'}), 400
        
        # Create language directory if it doesn't exist
        lang_dir = os.path.join(app.config['CODES_DIRECTORY'], language)
        try:
            os.makedirs(lang_dir, exist_ok=True)
        except OSError as e:
            app.logger.error(f"Failed to create directory {lang_dir}: {str(e)}")
            return jsonify({'error': 'Failed to create storage directory. The server may have limited write permissions.'}), 500
        
        # Load existing metadata
        metadata = load_code_metadata(language)
        
        uploaded_count = 0
        errors = []
        for file in files:
            if file and file.filename:
                # Secure the filename
                filename = file.filename
                # Basic validation of filename
                if not re.match(r'^[\w\-\.]+$', filename):
                    errors.append(f"{filename}: Invalid filename - contains invalid characters")
                    continue  # Skip invalid filenames
                
                # Check file extension matches language
                expected_ext = LANGUAGES[language]['extension']
                if not filename.endswith(expected_ext):
                    errors.append(f"{filename}: Wrong file extension - expected {expected_ext}")
                    continue  # Skip files with wrong extension
                
                filepath = os.path.join(lang_dir, filename)
                
                try:
                    # Handle encryption if requested
                    if encrypt:
                        # Read file content
                        file.seek(0)  # Reset file pointer to the beginning
                        content = file.read().decode('utf-8')
                        encrypted_data = encrypt_content_with_password(content, password)
                        # Save encrypted data
                        with open(filepath + '.enc', 'w') as f:
                            json.dump(encrypted_data, f)
                    else:
                        # Save the file normally
                        file.seek(0)  # Reset file pointer to the beginning
                        file.save(filepath)
                    
                    # Add to metadata
                    title = filename.rsplit('.', 1)[0].replace('_', ' ').title()
                    code_info = {
                        'title': title,
                        'description': f'Uploaded from file: {filename}',
                        'filename': filename,
                        'created_at': datetime.now().isoformat(),
                        'encrypted': encrypt,
                        'is_secret': is_secret
                    }
                    metadata.append(code_info)
                    uploaded_count += 1
                    
                    # Commit to GitHub if configured
                    if GITHUB_ENABLED and GITHUB_TOKEN:
                        try:
                            # Read the file content for GitHub commit
                            github_file_path = f"stored_codes/{language}/{filename}"
                            if encrypt:
                                github_file_path += '.enc'
                                github_content = json.dumps(encrypted_data, indent=2)
                            else:
                                with open(filepath, 'r') as f:
                                    github_content = f.read()
                            
                            commit_message = f"Add {language} file: {filename} via web upload"
                            commit_file_to_github(github_file_path, github_content, commit_message)
                            app.logger.info(f"Committed to GitHub: {github_file_path}")
                        except Exception as e:
                            app.logger.warning(f"File saved locally but GitHub commit failed for {filename}: {str(e)}")
                            # Don't fail the upload if GitHub commit fails
                    
                except UnicodeDecodeError as e:
                    errors.append(f"{filename}: File encoding error - must be UTF-8")
                    app.logger.error(f"Upload error for {filename}: {str(e)}")
                except PermissionError as e:
                    errors.append(f"{filename}: Permission denied - cannot write file")
                    app.logger.error(f"Upload error for {filename}: {str(e)}")
                except IOError as e:
                    errors.append(f"{filename}: File I/O error - {str(e)}")
                    app.logger.error(f"Upload error for {filename}: {str(e)}")
                except Exception as e:
                    errors.append(f"{filename}: {str(e)}")
                    app.logger.error(f"Upload error for {filename}: {str(e)}")
        
        # Save updated metadata
        if uploaded_count > 0:
            try:
                save_code_metadata(language, metadata)
                
                # Commit metadata to GitHub if configured
                if GITHUB_ENABLED and GITHUB_TOKEN:
                    try:
                        commit_metadata_to_github(language, metadata)
                        app.logger.info(f"Committed metadata to GitHub for {language}")
                    except Exception as e:
                        app.logger.warning(f"Metadata saved locally but GitHub commit failed: {str(e)}")
                        # Don't fail the upload if GitHub commit fails
                        
            except Exception as e:
                app.logger.error(f"Failed to save metadata: {str(e)}")
                return jsonify({'error': 'Files uploaded but failed to save metadata. Please try again.'}), 500
        
        if uploaded_count == 0:
            error_msg = 'No valid files were uploaded'
            if errors:
                error_msg += '. Errors: ' + '; '.join(errors[:5])  # Limit to first 5 errors
                if len(errors) > 5:
                    error_msg += f' (and {len(errors) - 5} more errors)'
            return jsonify({'error': error_msg}), 400
        
        return redirect(url_for('category', language=language))
    
    except Exception as e:
        app.logger.error(f"Unexpected error in upload_files: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred during file upload. Please try again.'}), 500

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
    
    # Read code content first
    with open(code_path, 'r') as f:
        code_content = f.read()
    
    # For compiled languages (C, C++, Java), use online compiler if local compiler is not available
    if language == 'c':
        compiler = lang_config['compiler']
        if not check_compiler_available(compiler):
            # Use online compiler for C code
            return execute_c_code_online(code_content, stdin_input)
    
    if language == 'cpp':
        compiler = lang_config['compiler']
        if not check_compiler_available(compiler):
            # Use online compiler for C++ code
            return execute_cpp_code_online(code_content, stdin_input)
    
    if language == 'java':
        compiler = lang_config['compiler']
        if not check_compiler_available(compiler):
            # Use online compiler for Java code
            return execute_java_code_online(code_content, stdin_input)
    
    # Check if compiler/interpreter is available for other languages
    if lang_config.get('compile'):
        compiler = lang_config['compiler']
        if not check_compiler_available(compiler):
            return f"Error: {compiler} compiler is not installed or not found in PATH. Please install {compiler} to execute {language} code."
    else:
        executor = lang_config['executor']
        if not check_compiler_available(executor):
            return f"Error: {executor} is not installed or not found in PATH. Please install {executor} to execute {language} code."
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy file to temp directory
        filename = os.path.basename(code_path)
        
        # SECURITY: Validate filename to prevent command injection
        # Only allow alphanumeric, underscore, dash, and appropriate extension
        # This validation occurs BEFORE any subprocess call
        import re
        if not re.match(r'^[\w\-]+\.(py|java|c|cpp|js|ts)$', filename):
            return "Error: Invalid filename"
        
        temp_file = os.path.join(tmpdir, filename)
        
        with open(temp_file, 'w') as f:
            f.write(code_content)
        
        try:
            # Compile if needed
            if lang_config['compile']:
                if language == 'java':
                    # Java compilation - using list form prevents shell injection
                    compile_cmd = [lang_config['compiler'], filename]
                    try:
                        compile_result = subprocess.run(
                            compile_cmd,
                            cwd=tmpdir,
                            capture_output=True,
                            text=True,
                            timeout=10,
                            shell=False  # Explicitly set shell=False for security
                        )
                    except FileNotFoundError:
                        return f"Error: {lang_config['compiler']} compiler not found. Please install Java JDK to compile Java code."
                    
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
                    try:
                        compile_result = subprocess.run(
                            compile_cmd,
                            cwd=tmpdir,
                            capture_output=True,
                            text=True,
                            timeout=10,
                            shell=False  # Explicitly set shell=False for security
                        )
                    except FileNotFoundError:
                        compiler_name = "GCC" if language == 'c' else "G++"
                        return f"Error: {lang_config['compiler']} compiler not found. Please install {compiler_name} to compile {language.upper()} code."
                    
                    if compile_result.returncode != 0:
                        return f"Compilation Error:\n{compile_result.stderr}"
                    
                    execute_cmd = [lang_config['executor']]
            else:
                # Python/JavaScript - direct execution using list form
                execute_cmd = [lang_config['executor'], filename]
            
            # Execute the code - using list form and shell=False for security
            try:
                result = subprocess.run(
                    execute_cmd,
                    cwd=tmpdir,
                    input=stdin_input,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False  # Explicitly set shell=False for security
                )
            except FileNotFoundError:
                executor_name = lang_config['executor']
                if language == 'python':
                    executor_name = "Python 3"
                elif language == 'java':
                    executor_name = "Java Runtime (JRE)"
                elif language == 'javascript':
                    executor_name = "Node.js"
                elif language == 'typescript':
                    executor_name = "ts-node"
                return f"Error: {lang_config['executor']} not found. Please install {executor_name} to execute {language} code."
            
            output = result.stdout
            if result.stderr:
                output += f"\nErrors/Warnings:\n{result.stderr}"
            
            return output
            
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out (5 seconds limit)"
        except Exception as e:
            return f"Error: {str(e)}"

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

# Error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file upload that exceeds size limit"""
    return jsonify({
        'error': 'File too large. Maximum upload size is 16MB.',
        'max_size': '16MB'
    }), 413

@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    app.logger.error(f'Internal server error: {error}')
    return jsonify({
        'error': 'An internal server error occurred. Please try again or contact support.',
        'message': 'Internal Server Error'
    }), 500

if __name__ == '__main__':
    # WARNING: debug=True is for development only. 
    # Set debug=False in production to prevent security vulnerabilities
    # Use environment variable to control debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
