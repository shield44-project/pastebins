# Backend Compiler Service

Production-ready backend service for compiling and executing C, C++, and Python code.

## 🚀 Features

- **Intelligent Compilation**: Tries multiple compiler strategies until code runs
- **Zero Warnings**: Automatically suppresses all warnings
- **Security**: Non-root container user, random temp files, timeout limits
- **Multi-Language**: Supports C, C++, and Python
- **Auto-Retry**: 8+ strategies for C, 10+ for C++

## 🏗️ Deployment

### Deploy on Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Set environment variable (optional):
```bash
railway variables set PORT=5000
```

Your backend will be available at: `https://your-app.railway.app`

### Deploy on Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `compiler-backend`
   - **Environment**: `Docker`
   - **Docker Command**: (auto-detected from Dockerfile)
4. Deploy!

Your backend will be available at: `https://your-app.onrender.com`

### Deploy on Fly.io

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Deploy:
```bash
cd compiler-backend
fly launch
fly deploy
```

## 🧪 Local Development

### Using Docker

```bash
cd compiler-backend
docker build -t code-runner .
docker run -p 5000:5000 code-runner
```

### Without Docker

```bash
cd compiler-backend
pip install -r requirements.txt
python app.py
```

## 📡 API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "service": "Code Runner Backend",
  "supported_languages": ["c", "cpp", "python"]
}
```

### `POST /run`
Execute code.

**Request:**
```json
{
  "language": "c",
  "code": "#include <stdio.h>\nint main() { printf(\"Hi\"); return 0; }",
  "input": ""
}
```

**Response (Success):**
```json
{
  "stdout": "Hi",
  "stderr": "",
  "error": null,
  "success": true,
  "compilation_info": "✅ Compiled successfully using: C11 standard"
}
```

**Response (Error):**
```json
{
  "stdout": "",
  "stderr": "error messages with AI suggestions...",
  "error": "Compilation failed",
  "success": false
}
```

## 🔒 Security Features

- **Non-root user**: Container runs as UID 1000
- **Random temp files**: Prevents conflicts and attacks  
- **Auto-cleanup**: Files deleted after execution
- **Timeout limits**: 10s for execution, 30s for compilation
- **Memory limits**: Configurable via Docker
- **Network isolation**: Can be disabled in Docker with `--network none`

## 🎯 Compiler Strategies

### C Compilation
1. Modern C11
2. Permissive C11 (warnings off)
3. GNU C11 with extensions
4. C99 fallback
5. GNU C99 extensions
6. C89 legacy
7. Maximum permissive mode
8. Default compiler behavior

### C++ Compilation
1. Modern C++23
2. Permissive C++23 (warnings off)
3. Modern C++20
4. Permissive C++20 (warnings off)
5. Modern C++17
6. Permissive C++17 (warnings off)
7. C++14 standard
8. C++11 standard
9. GNU C++23 with extensions
10. GNU C++20 with extensions
11. GNU C++17 with extensions
12. GNU C++14 with extensions
13. GNU C++11 with extensions
14. Maximum permissive mode
15. Legacy C++98
16. Default compiler behavior

## 📝 Environment Variables

- `PORT`: Server port (default: 5000)
- Railway and Render automatically set this

## 🐛 Troubleshooting

**Container fails to start:**
- Check that PORT is set correctly
- Verify Docker image built successfully

**Compilation errors:**
- System tries 8-10 strategies automatically
- Check stderr for detailed error messages

**Timeout errors:**
- Infinite loops or long-running code
- Adjust TIMEOUT_SECONDS in app.py if needed

## 📦 Dependencies

- Python 3.11+
- Flask 3.0.0
- flask-cors 4.0.0
- gcc (GNU C compiler)
- g++ (GNU C++ compiler)
- python3 (Python interpreter)
