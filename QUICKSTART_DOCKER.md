# Quick Start Guide - Docker Code Execution System

## 🚀 Quick Setup (3 Steps)

### 1. Build Docker Image
```bash
cd /home/runner/work/pastebins/pastebins
docker build -t code-sandbox:latest -f Dockerfile.sandbox .
```

### 2. Start Flask Server
```bash
python3 app.py
```

### 3. Test It!
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "code": "print(\"Hello World!\")"}'
```

## 📝 Quick Examples

### Python
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello from Python!\")"
  }'
```

### C
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "c",
    "code": "#include <stdio.h>\nint main() { printf(\"Hello from C!\\n\"); return 0; }"
  }'
```

### C++
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main() { std::cout << \"Hello from C++!\" << std::endl; return 0; }"
  }'
```

### With Input
```bash
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "name = input()\nprint(f\"Hello, {name}!\")",
    "input": "Alice"
  }'
```

## 🧪 Run Tests
```bash
python3 test_docker_executor.py
```

## 📚 More Examples
```bash
./sample_api_requests.sh
```

## 📖 Full Documentation
- **Complete Guide**: DOCKER_EXECUTOR_README.md
- **Implementation Details**: DOCKER_IMPLEMENTATION_SUMMARY.md
- **Test Suite**: test_docker_executor.py

## ✅ Verification
```bash
# Check Docker image
docker images | grep code-sandbox

# Run verification
python3 << 'EOF'
from docker_executor import execute_code_docker
result = execute_code_docker('python', 'print("Working!")')
print(result['stdout'])
EOF
```

## 🔒 Security Features
- ✅ 2 second CPU limit
- ✅ 256MB memory limit
- ✅ No internet access
- ✅ Non-root execution
- ✅ Auto cleanup
- ✅ Container isolation

## 🎯 Supported Languages
- **Python** (.py) - Direct execution
- **C** (.c) - Compiled with gcc
- **C++** (.cpp) - Compiled with g++

## ⚡ Performance
- Python: ~0.18s
- C: ~0.35s (compile + run)
- C++: ~0.58s (compile + run)

## 🆘 Troubleshooting

**Docker image not found?**
```bash
docker build -t code-sandbox:latest -f Dockerfile.sandbox .
```

**Flask not installed?**
```bash
pip3 install Flask Werkzeug cryptography requests
```

**Permission denied?**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 📞 Support
See DOCKER_EXECUTOR_README.md for full troubleshooting guide.

---
**Status**: ✅ Production Ready  
**Version**: 1.0  
**Last Updated**: 2025-11-17
