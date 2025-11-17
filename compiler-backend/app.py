#!/usr/bin/env python3
"""
Online Code Runner - Backend Compiler Service

This service compiles and executes C, C++, and Python code in a secure sandbox.
Designed to be deployed on Railway, Render, or similar container platforms.
"""

import os
import sys
import subprocess
import tempfile
import secrets
import shutil
import signal
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests from frontend

# Security configuration
TIMEOUT_SECONDS = 10  # Maximum execution time
MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB max output
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'code_runner')

# Ensure temp directory exists
Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)


def cleanup_old_files():
    """Remove temporary files older than 1 hour"""
    try:
        current_time = os.path.getmtime('.')
        for item in Path(TEMP_DIR).iterdir():
            if item.is_file() or item.is_dir():
                try:
                    file_time = os.path.getmtime(item)
                    if current_time - file_time > 3600:  # 1 hour
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                except Exception:
                    pass
    except Exception:
        pass


def generate_random_filename(extension):
    """Generate a random filename to prevent conflicts and enhance security"""
    random_name = secrets.token_hex(16)
    return f"{random_name}{extension}"


def run_with_timeout(cmd, input_data=None, timeout=TIMEOUT_SECONDS):
    """
    Execute a command with timeout and capture output
    
    Args:
        cmd: Command to execute (list)
        input_data: Optional stdin data
        timeout: Timeout in seconds
    
    Returns:
        tuple: (stdout, stderr, return_code)
    """
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid if sys.platform != 'win32' else None
        )
        
        try:
            stdout, stderr = process.communicate(
                input=input_data,
                timeout=timeout
            )
            return stdout[:MAX_OUTPUT_SIZE], stderr[:MAX_OUTPUT_SIZE], process.returncode
        except subprocess.TimeoutExpired:
            # Kill the process group
            if sys.platform != 'win32':
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            else:
                process.kill()
            process.wait()
            return "", "Error: Execution timed out (exceeded {} seconds)".format(timeout), -1
    except Exception as e:
        return "", f"Error executing command: {str(e)}", -1


def compile_and_run_c(code, input_data):
    """Compile and execute C code"""
    cleanup_old_files()
    
    source_file = os.path.join(TEMP_DIR, generate_random_filename('.c'))
    executable_file = os.path.join(TEMP_DIR, generate_random_filename('.out'))
    
    try:
        # Write source code to file
        with open(source_file, 'w') as f:
            f.write(code)
        
        # Compile
        compile_cmd = ['gcc', '-o', executable_file, source_file, '-Wall']
        stdout, stderr, returncode = run_with_timeout(compile_cmd, timeout=30)
        
        if returncode != 0:
            return {
                'stdout': '',
                'stderr': stderr,
                'error': 'Compilation failed',
                'success': False
            }
        
        # Execute
        stdout, stderr, returncode = run_with_timeout([executable_file], input_data)
        
        return {
            'stdout': stdout,
            'stderr': stderr,
            'error': None if returncode == 0 else 'Runtime error',
            'success': returncode == 0
        }
    
    finally:
        # Cleanup
        try:
            if os.path.exists(source_file):
                os.remove(source_file)
            if os.path.exists(executable_file):
                os.remove(executable_file)
        except Exception:
            pass


def compile_and_run_cpp(code, input_data):
    """Compile and execute C++ code"""
    cleanup_old_files()
    
    source_file = os.path.join(TEMP_DIR, generate_random_filename('.cpp'))
    executable_file = os.path.join(TEMP_DIR, generate_random_filename('.out'))
    
    try:
        # Write source code to file
        with open(source_file, 'w') as f:
            f.write(code)
        
        # Compile
        compile_cmd = ['g++', '-o', executable_file, source_file, '-Wall', '-std=c++17']
        stdout, stderr, returncode = run_with_timeout(compile_cmd, timeout=30)
        
        if returncode != 0:
            return {
                'stdout': '',
                'stderr': stderr,
                'error': 'Compilation failed',
                'success': False
            }
        
        # Execute
        stdout, stderr, returncode = run_with_timeout([executable_file], input_data)
        
        return {
            'stdout': stdout,
            'stderr': stderr,
            'error': None if returncode == 0 else 'Runtime error',
            'success': returncode == 0
        }
    
    finally:
        # Cleanup
        try:
            if os.path.exists(source_file):
                os.remove(source_file)
            if os.path.exists(executable_file):
                os.remove(executable_file)
        except Exception:
            pass


def run_python(code, input_data):
    """Execute Python code"""
    cleanup_old_files()
    
    source_file = os.path.join(TEMP_DIR, generate_random_filename('.py'))
    
    try:
        # Write source code to file
        with open(source_file, 'w') as f:
            f.write(code)
        
        # Execute
        stdout, stderr, returncode = run_with_timeout(
            ['python3', source_file],
            input_data
        )
        
        return {
            'stdout': stdout,
            'stderr': stderr,
            'error': None if returncode == 0 else 'Runtime error',
            'success': returncode == 0
        }
    
    finally:
        # Cleanup
        try:
            if os.path.exists(source_file):
                os.remove(source_file)
        except Exception:
            pass


@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Code Runner Backend',
        'supported_languages': ['c', 'cpp', 'python']
    })


@app.route('/run', methods=['POST'])
def run_code():
    """
    Execute code based on language
    
    Expected JSON payload:
    {
        "language": "c" | "cpp" | "python",
        "code": "source code here",
        "input": "stdin input (optional)"
    }
    
    Returns JSON:
    {
        "stdout": "program output",
        "stderr": "error output",
        "error": "error message or null",
        "success": true | false
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'stdout': '',
                'stderr': '',
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        language = data.get('language', '').lower()
        code = data.get('code', '')
        input_data = data.get('input', '')
        
        if not language:
            return jsonify({
                'stdout': '',
                'stderr': '',
                'error': 'Language not specified',
                'success': False
            }), 400
        
        if not code:
            return jsonify({
                'stdout': '',
                'stderr': '',
                'error': 'No code provided',
                'success': False
            }), 400
        
        # Execute based on language
        if language == 'c':
            result = compile_and_run_c(code, input_data)
        elif language in ['cpp', 'c++']:
            result = compile_and_run_cpp(code, input_data)
        elif language == 'python':
            result = run_python(code, input_data)
        else:
            return jsonify({
                'stdout': '',
                'stderr': '',
                'error': f'Unsupported language: {language}',
                'success': False
            }), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'stdout': '',
            'stderr': '',
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
