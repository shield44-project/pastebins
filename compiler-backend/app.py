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


def get_c_compiler_strategies():
    """
    Get list of compiler flag strategies to try for C code.
    Ordered from most strict to most permissive.
    """
    return [
        {
            'name': 'Modern C11',
            'flags': ['-std=c11', '-lm'],
            'description': 'C11 standard'
        },
        {
            'name': 'Permissive C11',
            'flags': ['-std=c11', '-lm', '-w'],
            'description': 'C11 with all warnings suppressed'
        },
        {
            'name': 'GNU C extensions',
            'flags': ['-std=gnu11', '-lm', '-w'],
            'description': 'GNU C11 with extensions and no warnings'
        },
        {
            'name': 'C99 fallback',
            'flags': ['-std=c99', '-lm', '-w'],
            'description': 'C99 standard with no warnings'
        },
        {
            'name': 'GNU C99 extensions',
            'flags': ['-std=gnu99', '-lm', '-w'],
            'description': 'GNU C99 with extensions'
        },
        {
            'name': 'C89 legacy',
            'flags': ['-std=c89', '-lm', '-w'],
            'description': 'Old C89 standard'
        },
        {
            'name': 'Maximum permissive',
            'flags': ['-w', '-fpermissive', '-lm'],
            'description': 'Most permissive settings'
        },
        {
            'name': 'No standard specified',
            'flags': ['-lm', '-w'],
            'description': 'Default compiler behavior with warnings off'
        }
    ]


def analyze_c_errors(stderr):
    """Analyze C compilation errors and provide helpful suggestions"""
    suggestions = []
    
    error_patterns = {
        'undeclared': {
            'pattern': ['undeclared', 'was not declared'],
            'suggestion': '💡 Variable or function not declared. Did you forget to:\n  - Declare the variable before using it?\n  - Include the required header file (e.g., #include <stdio.h>)?\n  - Check for typos in the variable/function name?'
        },
        'implicit_declaration': {
            'pattern': ['implicit declaration'],
            'suggestion': '💡 Function used without declaration. Add:\n  - #include <stdio.h> for printf, scanf\n  - #include <stdlib.h> for malloc, free\n  - #include <string.h> for string functions\n  - #include <math.h> for math functions'
        },
        'expected_semicolon': {
            'pattern': ['expected', 'before'],
            'suggestion': '💡 Syntax error detected. Common fixes:\n  - Add missing semicolon (;) at the end of the statement\n  - Check for missing closing braces }\n  - Verify parentheses are balanced'
        },
        'incompatible_types': {
            'pattern': ['incompatible', 'type'],
            'suggestion': '💡 Type mismatch. Try:\n  - Cast the value to the correct type\n  - Use correct format specifiers (%d for int, %f for float, %s for string)\n  - Verify function return types match expectations'
        },
        'undefined_reference': {
            'pattern': ['undefined reference'],
            'suggestion': '💡 Linking error. Solutions:\n  - Check if function is defined/implemented\n  - Verify library is linked correctly'
        }
    }
    
    stderr_lower = stderr.lower()
    for error_type, info in error_patterns.items():
        if any(pattern.lower() in stderr_lower for pattern in info['pattern']):
            suggestions.append(info['suggestion'])
    
    if suggestions:
        return '\n\n' + '\n\n'.join(suggestions)
    return ''


def compile_and_run_c(code, input_data):
    """
    Compile and execute C code with intelligent retry mechanism.
    Tries multiple compiler strategies until successful compilation.
    """
    cleanup_old_files()
    
    source_file = os.path.join(TEMP_DIR, generate_random_filename('.c'))
    executable_file = os.path.join(TEMP_DIR, generate_random_filename('.out'))
    
    try:
        # Write source code to file
        with open(source_file, 'w') as f:
            f.write(code)
        
        strategies = get_c_compiler_strategies()
        last_error = None
        compilation_attempts = []
        
        # Try each strategy until one succeeds
        for strategy in strategies:
            compile_cmd = ['gcc', '-o', executable_file, source_file] + strategy['flags']
            stdout, stderr, returncode = run_with_timeout(compile_cmd, timeout=30)
            
            compilation_attempts.append({
                'strategy': strategy['name'],
                'success': returncode == 0,
                'stderr': stderr[:200] if stderr else ''
            })
            
            if returncode == 0:
                # Compilation successful! Now execute
                stdout, stderr, returncode = run_with_timeout([executable_file], input_data)
                
                success_msg = f"✅ Compiled successfully using: {strategy['description']}"
                if len(compilation_attempts) > 1:
                    success_msg += f"\n🔄 Tried {len(compilation_attempts)} compiler strategies before success"
                
                return {
                    'stdout': stdout,
                    'stderr': stderr if stderr else '',
                    'error': None if returncode == 0 else 'Runtime error',
                    'success': returncode == 0,
                    'compilation_info': success_msg
                }
            
            last_error = stderr
        
        # All strategies failed
        error_msg = f"❌ Compilation failed after trying {len(strategies)} different strategies:\n\n"
        for i, attempt in enumerate(compilation_attempts, 1):
            error_msg += f"{i}. {attempt['strategy']}: Failed\n"
        
        error_msg += "\n" + "=" * 60 + "\n"
        error_msg += "Last error output:\n" + last_error
        error_msg += analyze_c_errors(last_error)
        
        return {
            'stdout': '',
            'stderr': error_msg,
            'error': 'Compilation failed with all strategies',
            'success': False
        }
    
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Internal error: {str(e)}',
            'error': 'Execution failed',
            'success': False
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


def get_cpp_compiler_strategies():
    """
    Get list of compiler flag strategies to try for C++ code.
    Ordered from most strict to most permissive.
    Now includes C++20 and C++23 support!
    """
    return [
        {
            'name': 'Modern C++23',
            'flags': ['-std=c++23', '-lm'],
            'description': 'C++23 standard'
        },
        {
            'name': 'Permissive C++23',
            'flags': ['-std=c++23', '-lm', '-w'],
            'description': 'C++23 with all warnings suppressed'
        },
        {
            'name': 'Modern C++20',
            'flags': ['-std=c++20', '-lm'],
            'description': 'C++20 standard'
        },
        {
            'name': 'Permissive C++20',
            'flags': ['-std=c++20', '-lm', '-w'],
            'description': 'C++20 with all warnings suppressed'
        },
        {
            'name': 'Modern C++17',
            'flags': ['-std=c++17', '-lm'],
            'description': 'C++17 standard'
        },
        {
            'name': 'Permissive C++17',
            'flags': ['-std=c++17', '-lm', '-w'],
            'description': 'C++17 with all warnings suppressed'
        },
        {
            'name': 'C++14 standard',
            'flags': ['-std=c++14', '-lm', '-w'],
            'description': 'C++14 standard with no warnings'
        },
        {
            'name': 'C++11 standard',
            'flags': ['-std=c++11', '-lm', '-w'],
            'description': 'C++11 standard with no warnings'
        },
        {
            'name': 'GNU C++23 extensions',
            'flags': ['-std=gnu++23', '-lm', '-w'],
            'description': 'GNU C++23 with extensions'
        },
        {
            'name': 'GNU C++20 extensions',
            'flags': ['-std=gnu++20', '-lm', '-w'],
            'description': 'GNU C++20 with extensions'
        },
        {
            'name': 'GNU C++17 extensions',
            'flags': ['-std=gnu++17', '-lm', '-w'],
            'description': 'GNU C++17 with extensions'
        },
        {
            'name': 'GNU C++14 extensions',
            'flags': ['-std=gnu++14', '-lm', '-w'],
            'description': 'GNU C++14 with extensions'
        },
        {
            'name': 'GNU C++11 extensions',
            'flags': ['-std=gnu++11', '-lm', '-w'],
            'description': 'GNU C++11 with extensions'
        },
        {
            'name': 'Maximum permissive',
            'flags': ['-w', '-fpermissive', '-lm'],
            'description': 'Most permissive C++ settings'
        },
        {
            'name': 'Legacy C++98',
            'flags': ['-std=c++98', '-w', '-fpermissive', '-lm'],
            'description': 'Old C++98 standard, very permissive'
        },
        {
            'name': 'No standard specified',
            'flags': ['-lm', '-w', '-fpermissive'],
            'description': 'Default compiler behavior, all warnings off'
        }
    ]


def analyze_cpp_errors(stderr):
    """Analyze C++ compilation errors and provide helpful suggestions"""
    suggestions = []
    
    error_patterns = {
        'undeclared': {
            'pattern': ['undeclared', 'was not declared', 'not declared in this scope'],
            'suggestion': '💡 Variable or function not declared. Did you forget to:\n  - Declare the variable before using it?\n  - Include the required header (e.g., #include <iostream>, #include <vector>)?\n  - Add "using namespace std;" or use std:: prefix?\n  - Check for typos in the identifier name?'
        },
        'no_match': {
            'pattern': ['no matching function', 'no match for'],
            'suggestion': '💡 Function signature mismatch. Try:\n  - Check the number and types of arguments\n  - Verify template parameters are correct\n  - Include the correct header file'
        },
        'expected_semicolon': {
            'pattern': ['expected', 'before'],
            'suggestion': '💡 Syntax error detected. Common fixes:\n  - Add missing semicolon (;)\n  - Check for missing closing braces }\n  - Verify template brackets <> are balanced'
        },
        'type_error': {
            'pattern': ['cannot convert', 'incompatible types', 'invalid conversion'],
            'suggestion': '💡 Type conversion error. Solutions:\n  - Use static_cast<type>(value) for explicit conversion\n  - Verify types match in assignment/comparison\n  - Check iterator types match container types'
        },
        'undefined_reference': {
            'pattern': ['undefined reference'],
            'suggestion': '💡 Linking error. Solutions:\n  - Implement all declared functions\n  - Link required libraries\n  - Check template instantiation'
        },
        'does_not_name': {
            'pattern': ['does not name a type'],
            'suggestion': '💡 Type not recognized. Check:\n  - Include proper header (#include <string> for std::string)\n  - Add "using namespace std;" or std:: prefix\n  - Forward declarations are complete'
        }
    }
    
    stderr_lower = stderr.lower()
    for error_type, info in error_patterns.items():
        if any(pattern.lower() in stderr_lower for pattern in info['pattern']):
            suggestions.append(info['suggestion'])
    
    if suggestions:
        return '\n\n' + '\n\n'.join(suggestions)
    return ''


def compile_and_run_cpp(code, input_data):
    """
    Compile and execute C++ code with intelligent retry mechanism.
    Tries multiple compiler strategies until successful compilation.
    """
    cleanup_old_files()
    
    source_file = os.path.join(TEMP_DIR, generate_random_filename('.cpp'))
    executable_file = os.path.join(TEMP_DIR, generate_random_filename('.out'))
    
    try:
        # Write source code to file
        with open(source_file, 'w') as f:
            f.write(code)
        
        strategies = get_cpp_compiler_strategies()
        last_error = None
        compilation_attempts = []
        
        # Try each strategy until one succeeds
        for strategy in strategies:
            compile_cmd = ['g++', '-o', executable_file, source_file] + strategy['flags']
            stdout, stderr, returncode = run_with_timeout(compile_cmd, timeout=30)
            
            compilation_attempts.append({
                'strategy': strategy['name'],
                'success': returncode == 0,
                'stderr': stderr[:200] if stderr else ''
            })
            
            if returncode == 0:
                # Compilation successful! Now execute
                stdout, stderr, returncode = run_with_timeout([executable_file], input_data)
                
                success_msg = f"✅ Compiled successfully using: {strategy['description']}"
                if len(compilation_attempts) > 1:
                    success_msg += f"\n🔄 Tried {len(compilation_attempts)} compiler strategies before success"
                
                return {
                    'stdout': stdout,
                    'stderr': stderr if stderr else '',
                    'error': None if returncode == 0 else 'Runtime error',
                    'success': returncode == 0,
                    'compilation_info': success_msg
                }
            
            last_error = stderr
        
        # All strategies failed
        error_msg = f"❌ Compilation failed after trying {len(strategies)} different strategies:\n\n"
        for i, attempt in enumerate(compilation_attempts, 1):
            error_msg += f"{i}. {attempt['strategy']}: Failed\n"
        
        error_msg += "\n" + "=" * 60 + "\n"
        error_msg += "Last error output:\n" + last_error
        error_msg += analyze_cpp_errors(last_error)
        
        return {
            'stdout': '',
            'stderr': error_msg,
            'error': 'Compilation failed with all strategies',
            'success': False
        }
    
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Internal error: {str(e)}',
            'error': 'Execution failed',
            'success': False
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
