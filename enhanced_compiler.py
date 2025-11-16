"""
Enhanced Compiler Module for C/C++
Provides improved compilation with better error handling, multiple standards support,
and compiler flags customization.
"""

import subprocess
import tempfile
import os
import shutil
import urllib.request
import urllib.parse
import json
from typing import Dict, List, Optional, Tuple


class CompilerResult:
    """Represents the result of a compilation/execution."""
    
    def __init__(self, success: bool, output: str, errors: str = "", 
                 compile_time: float = 0, execution_time: float = 0,
                 warnings: str = ""):
        self.success = success
        self.output = output
        self.errors = errors
        self.compile_time = compile_time
        self.execution_time = execution_time
        self.warnings = warnings
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            'success': self.success,
            'output': self.output,
            'errors': self.errors,
            'warnings': self.warnings,
            'compile_time': self.compile_time,
            'execution_time': self.execution_time
        }


class EnhancedCompiler:
    """
    Enhanced compiler for C and C++ with multiple backends,
    better error handling, and customizable compilation flags.
    """
    
    # Standard versions
    C_STANDARDS = ['c89', 'c99', 'c11', 'c17', 'c2x']
    CPP_STANDARDS = ['c++98', 'c++03', 'c++11', 'c++14', 'c++17', 'c++20', 'c++23']
    
    # Warning flags
    COMMON_WARNINGS = ['-Wall', '-Wextra', '-Wpedantic']
    
    def __init__(self):
        self.gcc_available = self._check_compiler_available('gcc')
        self.gpp_available = self._check_compiler_available('g++')
        self.clang_available = self._check_compiler_available('clang')
        self.clangpp_available = self._check_compiler_available('clang++')
    
    def _check_compiler_available(self, compiler: str) -> bool:
        """Check if a compiler is available."""
        return shutil.which(compiler) is not None
    
    def compile_and_run_c(self, code: str, stdin_input: str = "", 
                          standard: str = 'c11', 
                          optimization: str = '-O2',
                          extra_flags: List[str] = None,
                          use_warnings: bool = True) -> CompilerResult:
        """
        Compile and run C code with customizable options.
        
        Args:
            code: C source code
            stdin_input: Input to provide to the program
            standard: C standard version (c89, c99, c11, c17, c2x)
            optimization: Optimization level (-O0, -O1, -O2, -O3, -Os)
            extra_flags: Additional compiler flags
            use_warnings: Whether to enable warning flags
        
        Returns:
            CompilerResult with execution results
        """
        # Try local compilation first
        if self.gcc_available:
            return self._compile_and_run_local_c(
                code, stdin_input, standard, optimization, extra_flags, use_warnings
            )
        elif self.clang_available:
            return self._compile_and_run_local_c(
                code, stdin_input, standard, optimization, extra_flags, use_warnings, 
                compiler='clang'
            )
        else:
            # Fall back to online compiler
            return self._compile_and_run_online(code, stdin_input, 'c')
    
    def compile_and_run_cpp(self, code: str, stdin_input: str = "",
                            standard: str = 'c++17',
                            optimization: str = '-O2',
                            extra_flags: List[str] = None,
                            use_warnings: bool = True) -> CompilerResult:
        """
        Compile and run C++ code with customizable options.
        
        Args:
            code: C++ source code
            stdin_input: Input to provide to the program
            standard: C++ standard version (c++98, c++11, c++14, c++17, c++20, c++23)
            optimization: Optimization level (-O0, -O1, -O2, -O3, -Os)
            extra_flags: Additional compiler flags
            use_warnings: Whether to enable warning flags
        
        Returns:
            CompilerResult with execution results
        """
        # Try local compilation first
        if self.gpp_available:
            return self._compile_and_run_local_cpp(
                code, stdin_input, standard, optimization, extra_flags, use_warnings
            )
        elif self.clangpp_available:
            return self._compile_and_run_local_cpp(
                code, stdin_input, standard, optimization, extra_flags, use_warnings,
                compiler='clang++'
            )
        else:
            # Fall back to online compiler
            return self._compile_and_run_online(code, stdin_input, 'cpp')
    
    def _compile_and_run_local_c(self, code: str, stdin_input: str,
                                  standard: str, optimization: str,
                                  extra_flags: List[str], use_warnings: bool,
                                  compiler: str = 'gcc') -> CompilerResult:
        """Compile and run C code locally."""
        import time
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write source file
            source_file = os.path.join(tmpdir, 'program.c')
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Build compilation command
            executable = os.path.join(tmpdir, 'program')
            compile_cmd = [compiler, source_file, '-o', executable]
            
            # Add standard flag
            if standard:
                compile_cmd.append(f'-std={standard}')
            
            # Add optimization flag
            if optimization:
                compile_cmd.append(optimization)
            
            # Add warning flags
            if use_warnings:
                compile_cmd.extend(self.COMMON_WARNINGS)
            
            # Add extra flags
            if extra_flags:
                compile_cmd.extend(extra_flags)
            
            try:
                # Compile
                start_time = time.time()
                compile_result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    shell=False
                )
                compile_time = time.time() - start_time
                
                if compile_result.returncode != 0:
                    # Compilation failed
                    error_msg = self._format_compile_errors(compile_result.stderr, 'c')
                    return CompilerResult(
                        success=False,
                        output="",
                        errors=error_msg,
                        compile_time=compile_time
                    )
                
                # Get warnings if any
                warnings = compile_result.stderr if compile_result.stderr else ""
                
                # Execute
                start_time = time.time()
                exec_result = subprocess.run(
                    [executable],
                    input=stdin_input,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False
                )
                execution_time = time.time() - start_time
                
                return CompilerResult(
                    success=True,
                    output=exec_result.stdout,
                    errors=exec_result.stderr if exec_result.stderr else "",
                    warnings=warnings,
                    compile_time=compile_time,
                    execution_time=execution_time
                )
                
            except subprocess.TimeoutExpired:
                return CompilerResult(
                    success=False,
                    output="",
                    errors="Error: Execution timed out (maximum 5 seconds)"
                )
            except Exception as e:
                return CompilerResult(
                    success=False,
                    output="",
                    errors=f"Error: {str(e)}"
                )
    
    def _compile_and_run_local_cpp(self, code: str, stdin_input: str,
                                    standard: str, optimization: str,
                                    extra_flags: List[str], use_warnings: bool,
                                    compiler: str = 'g++') -> CompilerResult:
        """Compile and run C++ code locally."""
        import time
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write source file
            source_file = os.path.join(tmpdir, 'program.cpp')
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Build compilation command
            executable = os.path.join(tmpdir, 'program')
            compile_cmd = [compiler, source_file, '-o', executable]
            
            # Add standard flag
            if standard:
                compile_cmd.append(f'-std={standard}')
            
            # Add optimization flag
            if optimization:
                compile_cmd.append(optimization)
            
            # Add warning flags
            if use_warnings:
                compile_cmd.extend(self.COMMON_WARNINGS)
            
            # Add extra flags
            if extra_flags:
                compile_cmd.extend(extra_flags)
            
            try:
                # Compile
                start_time = time.time()
                compile_result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    shell=False
                )
                compile_time = time.time() - start_time
                
                if compile_result.returncode != 0:
                    # Compilation failed
                    error_msg = self._format_compile_errors(compile_result.stderr, 'cpp')
                    return CompilerResult(
                        success=False,
                        output="",
                        errors=error_msg,
                        compile_time=compile_time
                    )
                
                # Get warnings if any
                warnings = compile_result.stderr if compile_result.stderr else ""
                
                # Execute
                start_time = time.time()
                exec_result = subprocess.run(
                    [executable],
                    input=stdin_input,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False
                )
                execution_time = time.time() - start_time
                
                return CompilerResult(
                    success=True,
                    output=exec_result.stdout,
                    errors=exec_result.stderr if exec_result.stderr else "",
                    warnings=warnings,
                    compile_time=compile_time,
                    execution_time=execution_time
                )
                
            except subprocess.TimeoutExpired:
                return CompilerResult(
                    success=False,
                    output="",
                    errors="Error: Execution timed out (maximum 5 seconds)"
                )
            except Exception as e:
                return CompilerResult(
                    success=False,
                    output="",
                    errors=f"Error: {str(e)}"
                )
    
    def _compile_and_run_online(self, code: str, stdin_input: str, 
                                 language: str) -> CompilerResult:
        """
        Compile and run code using online compiler (Wandbox API).
        
        Args:
            code: Source code
            stdin_input: Input for the program
            language: 'c' or 'cpp'
        
        Returns:
            CompilerResult with execution results
        """
        try:
            url = 'https://wandbox.org/api/compile.json'
            
            compiler_map = {
                'c': 'gcc-head',
                'cpp': 'clang-head'
            }
            
            compiler_options = {
                'c': '-Wall -O2 -std=c11',
                'cpp': '-Wall -O2 -std=c++17'
            }
            
            payload = {
                'compiler': compiler_map.get(language, 'gcc-head'),
                'code': code,
                'stdin': stdin_input,
                'options': '',
                'compiler-option-raw': compiler_options.get(language, ''),
                'runtime-option-raw': '',
                'save': False
            }
            
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
                
                # Check for compilation error
                if 'compiler_error' in result and result['compiler_error']:
                    error_msg = self._format_compile_errors(result['compiler_error'], language)
                    return CompilerResult(
                        success=False,
                        output="",
                        errors=error_msg
                    )
                
                # Get warnings
                warnings = result.get('compiler_message', '')
                
                # Get output
                output = result.get('program_output', '')
                errors = result.get('program_error', '')
                
                # Check status
                status = result.get('status', '0')
                if status != '0' and not output and not errors:
                    errors = f"Program exited with status {status}"
                
                return CompilerResult(
                    success=True,
                    output=output,
                    errors=errors,
                    warnings=warnings
                )
                
        except urllib.error.URLError as e:
            return CompilerResult(
                success=False,
                output="",
                errors=f"Error: Unable to connect to online compiler service.\nDetails: {str(e)}"
            )
        except Exception as e:
            return CompilerResult(
                success=False,
                output="",
                errors=f"Error: {str(e)}"
            )
    
    def _format_compile_errors(self, error_text: str, language: str) -> str:
        """
        Format compiler errors to be more user-friendly.
        
        Args:
            error_text: Raw compiler error output
            language: 'c' or 'cpp'
        
        Returns:
            Formatted error message with helpful hints
        """
        lines = error_text.strip().split('\n')
        formatted = ["Compilation Errors:"]
        formatted.append("=" * 60)
        
        # Add helpful context for common errors
        error_hints = {
            'expected \';\' before': 'Missing semicolon',
            'undeclared': 'Variable or function not declared',
            'expected \')\' before': 'Missing closing parenthesis',
            'expected \'}\' before': 'Missing closing brace',
            'implicit declaration': 'Function used without declaration/include',
            'conflicting types': 'Function declaration doesn\'t match definition',
            'incompatible types': 'Type mismatch in assignment or parameter',
            'undefined reference': 'Function declared but not defined'
        }
        
        for line in lines:
            formatted.append(line)
            
            # Add hints for common errors
            for error_pattern, hint in error_hints.items():
                if error_pattern in line.lower():
                    formatted.append(f"  💡 Hint: {hint}")
                    break
        
        formatted.append("=" * 60)
        return '\n'.join(formatted)
    
    def get_compiler_info(self) -> Dict:
        """Get information about available compilers."""
        info = {
            'gcc': {
                'available': self.gcc_available,
                'version': self._get_compiler_version('gcc') if self.gcc_available else None
            },
            'g++': {
                'available': self.gpp_available,
                'version': self._get_compiler_version('g++') if self.gpp_available else None
            },
            'clang': {
                'available': self.clang_available,
                'version': self._get_compiler_version('clang') if self.clang_available else None
            },
            'clang++': {
                'available': self.clangpp_available,
                'version': self._get_compiler_version('clang++') if self.clangpp_available else None
            },
            'online': {
                'available': True,
                'service': 'Wandbox'
            }
        }
        return info
    
    def _get_compiler_version(self, compiler: str) -> Optional[str]:
        """Get version of a compiler."""
        try:
            result = subprocess.run(
                [compiler, '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False
            )
            if result.returncode == 0:
                # Get first line which usually contains version
                return result.stdout.split('\n')[0]
        except:
            pass
        return None
