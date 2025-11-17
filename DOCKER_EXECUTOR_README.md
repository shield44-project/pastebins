# Docker-Based Secure Code Execution System

## Overview

This system provides secure, sandboxed code execution for C, C++, and Python using Docker containers. It implements strict resource limits and security constraints to prevent abuse.

## Features

- **Multi-language Support**: C (gcc), C++ (g++), Python 3
- **Security**:
  - Isolated Docker containers
  - No internet access (--network none)
  - Non-root user execution
  - CPU time limit: 2 seconds
  - Memory limit: 256MB
  - Process limit: 50 processes max
  - Automatic cleanup after execution
- **Resource Management**:
  - CPU time limit enforced via ulimit
  - Memory limit enforced via Docker
  - Wall time timeout protection
  - Automatic container cleanup

## Architecture

### Components

1. **Dockerfile.sandbox**: Ubuntu-based image with gcc, g++, and Python3
2. **docker_executor.py**: Python module for Docker-based code execution
3. **app.py**: Flask API endpoint (`/api/execute`)

### Security Measures

1. **Container Isolation**: Each execution runs in a fresh, isolated Docker container
2. **No Network Access**: `--network none` flag prevents internet access
3. **Resource Limits**:
   - CPU: Limited to 2 seconds of CPU time
   - Memory: 256MB hard limit
   - Swap: Disabled
   - Processes: Max 50 PIDs
4. **Non-Root User**: Code runs as user `sandbox` (UID 1000), not root
5. **Timeout Protection**: Wall-time timeout prevents hanging processes
6. **Auto Cleanup**: Containers are automatically removed after execution (`--rm`)

## API Endpoint

### POST /api/execute

Execute code in a secure Docker sandbox.

#### Request

```json
{
  "language": "c" | "cpp" | "python",
  "code": "source code string",
  "input": "optional stdin input (optional)"
}
```

#### Response

```json
{
  "success": true | false,
  "stdout": "program output",
  "stderr": "error messages",
  "compile_errors": "compilation errors (for C/C++)",
  "execution_time": 0.123
}
```

## Usage Examples

### Python Execution

**Basic Hello World:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello from Python!\")\nprint(\"2 + 2 =\", 2 + 2)"
  }'
```

**Response:**
```json
{
  "success": true,
  "stdout": "Hello from Python!\n2 + 2 = 4\n",
  "stderr": "",
  "compile_errors": "",
  "execution_time": 0.234
}
```

**With Input:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "name = input()\nprint(f\"Hello, {name}!\")",
    "input": "Alice"
  }'
```

### C Execution

**Basic Hello World:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    printf(\"Hello from C!\\n\");\n    return 0;\n}"
  }'
```

**Response:**
```json
{
  "success": true,
  "stdout": "Hello from C!\n",
  "stderr": "",
  "compile_errors": "",
  "execution_time": 0.456
}
```

**With Input:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    int a, b;\n    scanf(\"%d %d\", &a, &b);\n    printf(\"Sum: %d\\n\", a + b);\n    return 0;\n}",
    "input": "5 10"
  }'
```

**Response:**
```json
{
  "success": true,
  "stdout": "Sum: 15\n",
  "stderr": "",
  "compile_errors": "",
  "execution_time": 0.512
}
```

**Compilation Error:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() {\n    printf(\"Missing semicolon\")\n    return 0;\n}"
  }'
```

**Response:**
```json
{
  "success": false,
  "stdout": "",
  "stderr": "",
  "compile_errors": "program.c: In function 'main':\nprogram.c:3:35: error: expected ';' before 'return'\n    3 |     printf(\"Missing semicolon\")\n      |                                   ^\n      |                                   ;\n    4 |     return 0;\n      |     ~~~~~~\n",
  "execution_time": 0.234
}
```

### C++ Execution

**Basic Hello World:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main() {\n    std::cout << \"Hello from C++!\" << std::endl;\n    return 0;\n}"
  }'
```

**With STL:**
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\n#include <vector>\nint main() {\n    std::vector<int> nums = {1, 2, 3, 4, 5};\n    int sum = 0;\n    for (int n : nums) sum += n;\n    std::cout << \"Sum: \" << sum << std::endl;\n    return 0;\n}"
  }'
```

## Python Code Example

```python
import requests
import json

def execute_code(language, code, stdin_input=""):
    """Execute code using the Docker API."""
    url = "http://localhost:5000/api/execute"
    
    payload = {
        "language": language,
        "code": code,
        "input": stdin_input
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Example usage
if __name__ == "__main__":
    # Python code
    result = execute_code("python", "print('Hello from Python!')")
    print(f"Python: {result['stdout']}")
    
    # C code
    c_code = """
#include <stdio.h>
int main() {
    printf("Hello from C!\\n");
    return 0;
}
"""
    result = execute_code("c", c_code)
    print(f"C: {result['stdout']}")
    
    # C++ code
    cpp_code = """
#include <iostream>
int main() {
    std::cout << "Hello from C++!" << std::endl;
    return 0;
}
"""
    result = execute_code("cpp", cpp_code)
    print(f"C++: {result['stdout']}")
```

## Node.js Code Example

```javascript
const axios = require('axios');

async function executeCode(language, code, input = '') {
  try {
    const response = await axios.post('http://localhost:5000/api/execute', {
      language: language,
      code: code,
      input: input
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}

// Example usage
(async () => {
  // Python code
  let result = await executeCode('python', 'print("Hello from Python!")');
  console.log('Python:', result.stdout);
  
  // C code
  const cCode = `
#include <stdio.h>
int main() {
    printf("Hello from C!\\n");
    return 0;
}
`;
  result = await executeCode('c', cCode);
  console.log('C:', result.stdout);
  
  // C++ code
  const cppCode = `
#include <iostream>
int main() {
    std::cout << "Hello from C++!" << std::endl;
    return 0;
}
`;
  result = await executeCode('cpp', cppCode);
  console.log('C++:', result.stdout);
})();
```

## Installation & Setup

### Prerequisites

- Docker installed and running
- Python 3.8+
- Flask and required dependencies

### Build Docker Image

The Docker image is automatically built on first use, or you can build it manually:

```bash
docker build -t code-sandbox:latest -f Dockerfile.sandbox .
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`.

## Testing

Run the test suite:

```bash
python test_docker_executor.py
```

This will test:
- Docker executor initialization
- Python, C, and C++ execution
- Input handling
- Error handling (compilation and runtime)
- Timeout protection

## Security Considerations

### What's Protected

✅ Network access disabled  
✅ CPU time limited (2 seconds)  
✅ Memory limited (256MB)  
✅ Process count limited (50)  
✅ Non-root execution  
✅ Automatic cleanup  
✅ Isolated filesystem  

### What's NOT Protected

⚠️ Disk I/O limits not enforced  
⚠️ No rate limiting on API (add in production)  
⚠️ No authentication/authorization (add in production)  

### Production Recommendations

1. **Add Rate Limiting**: Limit requests per IP/user
2. **Add Authentication**: Require API keys or OAuth
3. **Monitor Resources**: Track CPU/memory usage across all containers
4. **Add Logging**: Log all executions for security auditing
5. **Use HTTPS**: Enable SSL/TLS in production
6. **Container Registry**: Use a private registry for the Docker image
7. **Update Regularly**: Keep base image and compilers updated

## Error Handling

### Compilation Errors (C/C++)

When C/C++ code fails to compile, the response includes detailed compiler output in `compile_errors`:

```json
{
  "success": false,
  "stdout": "",
  "stderr": "",
  "compile_errors": "program.c:3:35: error: expected ';' before 'return'",
  "execution_time": 0.234
}
```

### Runtime Errors

Runtime errors are captured in `stderr`:

```json
{
  "success": true,
  "stdout": "",
  "stderr": "Traceback (most recent call last):\n  File \"script.py\", line 1, in <module>\n    x = 1 / 0\nZeroDivisionError: division by zero\n",
  "compile_errors": "",
  "execution_time": 0.123
}
```

### Timeout Errors

Code that exceeds the 2-second CPU limit:

```json
{
  "success": false,
  "stdout": "",
  "stderr": "Execution timed out (exceeded 2 second CPU limit)",
  "compile_errors": "",
  "execution_time": 2.0
}
```

## Troubleshooting

### Docker Image Build Fails

```bash
# Check Docker is running
docker ps

# Build manually with verbose output
docker build -t code-sandbox:latest -f Dockerfile.sandbox . --no-cache
```

### Permission Denied Errors

```bash
# Ensure Docker is running without sudo (add user to docker group)
sudo usermod -aG docker $USER
newgrp docker
```

### Container Doesn't Start

```bash
# Check Docker logs
docker logs <container-id>

# Check available disk space
df -h

# Clean up old containers
docker system prune -a
```

## License

This project is open source and available under the MIT License.
