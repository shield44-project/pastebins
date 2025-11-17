"""
Docker-based secure code execution system.
Provides sandboxed execution for C, C++, and Python3 with resource limits.
"""

import subprocess
import tempfile
import os
import time
import json
from typing import Dict, Optional, Tuple


class DockerExecutor:
    """
    Secure code executor using Docker containers.
    Supports C, C++, and Python3 with strict resource limits.
    """
    
    # Docker image name
    IMAGE_NAME = "code-sandbox:latest"
    
    # Resource limits
    CPU_LIMIT = 2  # seconds (CPU time, not wall time)
    MEMORY_LIMIT = "256m"  # 256 MB
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['c', 'cpp', 'python']
    
    def __init__(self):
        """Initialize the Docker executor."""
        self.image_built = self._check_or_build_image()
    
    def _check_or_build_image(self) -> bool:
        """Check if Docker image exists, build if not."""
        try:
            # Check if image exists
            result = subprocess.run(
                ['docker', 'images', '-q', self.IMAGE_NAME],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout.strip():
                return True
            
            # Image doesn't exist, build it
            print(f"Building Docker image {self.IMAGE_NAME}...")
            dockerfile_path = os.path.join(
                os.path.dirname(__file__), 
                'Dockerfile.sandbox'
            )
            
            if not os.path.exists(dockerfile_path):
                print(f"Error: Dockerfile not found at {dockerfile_path}")
                return False
            
            build_result = subprocess.run(
                ['docker', 'build', '-t', self.IMAGE_NAME, '-f', dockerfile_path, '.'],
                cwd=os.path.dirname(__file__),
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes for build
            )
            
            if build_result.returncode != 0:
                print(f"Error building Docker image: {build_result.stderr}")
                return False
            
            print(f"Docker image {self.IMAGE_NAME} built successfully")
            return True
            
        except subprocess.TimeoutExpired:
            print("Error: Docker build/check timed out")
            return False
        except FileNotFoundError:
            print("Error: Docker not found. Please install Docker.")
            return False
        except Exception as e:
            print(f"Error checking/building Docker image: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Docker executor is available."""
        return self.image_built
    
    def execute(self, language: str, code: str, stdin_input: str = "") -> Dict:
        """
        Execute code in a secure Docker container.
        
        Args:
            language: Programming language ('c', 'cpp', 'python')
            code: Source code to execute
            stdin_input: Input to provide to the program
        
        Returns:
            Dictionary with:
                - success: bool
                - stdout: program output
                - stderr: error messages
                - compile_errors: compilation errors (for C/C++)
                - execution_time: time taken
        """
        if not self.image_built:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Docker image not available',
                'compile_errors': '',
                'execution_time': 0
            }
        
        if language not in self.SUPPORTED_LANGUAGES:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Unsupported language: {language}',
                'compile_errors': '',
                'execution_time': 0
            }
        
        # Choose execution method based on language
        if language == 'c':
            return self._execute_c(code, stdin_input)
        elif language == 'cpp':
            return self._execute_cpp(code, stdin_input)
        elif language == 'python':
            return self._execute_python(code, stdin_input)
    
    def _execute_c(self, code: str, stdin_input: str) -> Dict:
        """Execute C code."""
        return self._execute_compiled(code, stdin_input, 'gcc', 'program.c', 'c')
    
    def _execute_cpp(self, code: str, stdin_input: str) -> Dict:
        """Execute C++ code."""
        return self._execute_compiled(code, stdin_input, 'g++', 'program.cpp', 'cpp')
    
    def _execute_compiled(self, code: str, stdin_input: str, 
                          compiler: str, source_file: str, language: str) -> Dict:
        """
        Execute C or C++ code (compile first, then run).
        
        Args:
            code: Source code
            stdin_input: Input for the program
            compiler: 'gcc' or 'g++'
            source_file: Name of source file
            language: 'c' or 'cpp'
        
        Returns:
            Execution result dictionary
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Make tmpdir accessible to Docker
            os.chmod(tmpdir, 0o777)
            
            # Write source file
            source_path = os.path.join(tmpdir, source_file)
            with open(source_path, 'w') as f:
                f.write(code)
            
            # Write input file if provided
            input_path = os.path.join(tmpdir, 'input.txt')
            with open(input_path, 'w') as f:
                f.write(stdin_input)
            
            # Make files readable/writable by all users (for Docker container access)
            os.chmod(source_path, 0o666)
            os.chmod(input_path, 0o666)
            
            # Compile inside Docker
            compile_start = time.time()
            compile_cmd = [
                'docker', 'run',
                '--rm',
                '--network', 'none',  # No internet access
                '--memory', self.MEMORY_LIMIT,
                '--memory-swap', self.MEMORY_LIMIT,  # No swap
                '--cpus', '1',  # Limit CPU cores
                '--pids-limit', '50',  # Limit number of processes
                '-v', f'{tmpdir}:/sandbox:rw',
                '-w', '/sandbox',
                # Note: Compilation runs as root to write executable, execution will run as sandbox user
                self.IMAGE_NAME,
                compiler, source_file, '-o', 'program', '-O2', '-std=c11' if language == 'c' else '-std=c++17'
            ]
            
            try:
                compile_result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 seconds for compilation
                )
                compile_time = time.time() - compile_start
                
                if compile_result.returncode != 0:
                    # Compilation failed
                    return {
                        'success': False,
                        'stdout': '',
                        'stderr': '',
                        'compile_errors': compile_result.stderr,
                        'execution_time': compile_time
                    }
                
                # Run the compiled program
                exec_start = time.time()
                exec_cmd = [
                    'docker', 'run',
                    '--rm',
                    '--network', 'none',  # No internet
                    '--memory', self.MEMORY_LIMIT,
                    '--memory-swap', self.MEMORY_LIMIT,
                    '--cpus', '1',
                    '--pids-limit', '50',
                    '--ulimit', f'cpu={self.CPU_LIMIT}',  # CPU time limit
                    '-v', f'{tmpdir}:/sandbox:rw',  # Read-write mount (but execution is still sandboxed)
                    '-w', '/sandbox',
                    '--user', 'sandbox',  # Run as non-root user
                    self.IMAGE_NAME,
                    'sh', '-c', './program < input.txt'
                ]
                
                exec_result = subprocess.run(
                    exec_cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.CPU_LIMIT + 2  # Wall time limit (slightly more than CPU limit)
                )
                exec_time = time.time() - exec_start
                
                return {
                    'success': True,
                    'stdout': exec_result.stdout,
                    'stderr': exec_result.stderr,
                    'compile_errors': '',
                    'execution_time': compile_time + exec_time
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': 'Execution timed out (exceeded 2 second CPU limit)',
                    'compile_errors': '',
                    'execution_time': self.CPU_LIMIT
                }
            except Exception as e:
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': f'Execution error: {str(e)}',
                    'compile_errors': '',
                    'execution_time': 0
                }
    
    def _execute_python(self, code: str, stdin_input: str) -> Dict:
        """Execute Python3 code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Make tmpdir accessible to Docker
            os.chmod(tmpdir, 0o777)
            
            # Write Python file
            script_path = os.path.join(tmpdir, 'script.py')
            with open(script_path, 'w') as f:
                f.write(code)
            
            # Write input file
            input_path = os.path.join(tmpdir, 'input.txt')
            with open(input_path, 'w') as f:
                f.write(stdin_input)
            
            # Make files readable by all users
            os.chmod(script_path, 0o666)
            os.chmod(input_path, 0o666)
            
            # Execute Python script
            exec_start = time.time()
            exec_cmd = [
                'docker', 'run',
                '--rm',
                '--network', 'none',  # No internet
                '--memory', self.MEMORY_LIMIT,
                '--memory-swap', self.MEMORY_LIMIT,
                '--cpus', '1',
                '--pids-limit', '50',
                '--ulimit', f'cpu={self.CPU_LIMIT}',  # CPU time limit
                '-v', f'{tmpdir}:/sandbox:rw',  # Read-write mount (but execution is still sandboxed)
                '-w', '/sandbox',
                '--user', 'sandbox',  # Run as non-root user
                self.IMAGE_NAME,
                'sh', '-c', 'python3 script.py < input.txt'
            ]
            
            try:
                exec_result = subprocess.run(
                    exec_cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.CPU_LIMIT + 2  # Wall time limit
                )
                exec_time = time.time() - exec_start
                
                return {
                    'success': True,
                    'stdout': exec_result.stdout,
                    'stderr': exec_result.stderr,
                    'compile_errors': '',
                    'execution_time': exec_time
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': 'Execution timed out (exceeded 2 second CPU limit)',
                    'compile_errors': '',
                    'execution_time': self.CPU_LIMIT
                }
            except Exception as e:
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': f'Execution error: {str(e)}',
                    'compile_errors': '',
                    'execution_time': 0
                }


# Global instance
_docker_executor = None


def get_docker_executor() -> DockerExecutor:
    """Get or create global Docker executor instance."""
    global _docker_executor
    if _docker_executor is None:
        _docker_executor = DockerExecutor()
    return _docker_executor


def execute_code_docker(language: str, code: str, stdin_input: str = "") -> Dict:
    """
    Convenience function to execute code using Docker.
    
    Args:
        language: Programming language ('c', 'cpp', 'python')
        code: Source code
        stdin_input: Input for the program
    
    Returns:
        Execution result dictionary
    """
    executor = get_docker_executor()
    return executor.execute(language, code, stdin_input)
