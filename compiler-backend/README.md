# Backend Compiler Service

Production-ready backend service for compiling and executing C, C++, and Python code.

## 🚀 Features

- **Minimal Compilation**: Simple, clean commands compatible with Vercel/Clang
- **Clang/Clang++ Compiler**: Uses clang for C++20/C++23 support
- **No Extra Flags**: Only standard version flags (no -Wall, -O2, -stdlib, etc.)
- **Security**: Non-root container user, random temp files, timeout limits
- **Multi-Language**: Supports C, C++, and Python
- **Auto-Retry**: 4 strategies for C, 6 for C++
- **Modern C++ Standards**: C++11, C++14, C++17, C++20, and C++23

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

### C Compilation (using clang)
Minimal flags for Vercel compatibility:
1. C11 standard: `clang -std=c11 input.c -o output`
2. C99 standard: `clang -std=c99 input.c -o output`
3. C89 standard: `clang -std=c89 input.c -o output`
4. Default: `clang input.c -o output`

### C++ Compilation (using clang++)
Minimal flags for Vercel compatibility:
1. C++23 standard: `clang++ -std=c++23 input.cpp -o output`
2. C++20 standard: `clang++ -std=c++20 input.cpp -o output`
3. C++17 standard: `clang++ -std=c++17 input.cpp -o output`
4. C++14 standard: `clang++ -std=c++14 input.cpp -o output`
5. C++11 standard: `clang++ -std=c++11 input.cpp -o output`
6. Default: `clang++ input.cpp -o output`

**Note**: No additional flags like -Wall, -O2, -stdlib=libc++, -lm are used for maximum compatibility with Vercel's environment.

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
- clang (C compiler)
- clang++ (C++ compiler with C++11/14/17/20/23 support)
- python3 (Python interpreter)
