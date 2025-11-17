# 🚀 Online Code Runner

A full-stack online code compiler and executor for C, C++, and Python with **deployment-optimized architecture**.

**Frontend**: Next.js (Vercel) → **Backend**: Flask with Docker (Railway/Render)

## ✨ Features

### 🎯 Intelligent Compilation
- **Auto-retry system**: Tries 8+ compiler strategies for C, 10+ for C++
- **Zero warnings**: Automatically suppresses all compiler warnings  
- **AI error analysis**: Provides helpful suggestions when compilation fails
- **Multiple standards**: C89/C99/C11/GNU C and C++98/C++11/C++14/C++17/GNU C++

### 🔒 Production Security
- Non-root Docker container (UID 1000)
- Random temp filenames to prevent conflicts
- Automatic file cleanup (1hr TTL)
- 10s execution timeout, 30s compilation timeout
- 1MB output size limit
- Network isolation capable

### 🎨 Modern Frontend
- Beautiful, responsive UI with Tailwind CSS
- Real-time execution feedback
- Syntax-aware code editor
- Clear success/error indicators
- Mobile-friendly design

## 📁 Project Structure

```
online-code-runner/
├── compiler-backend/       # Backend compiler service
│   ├── app.py             # Flask API with intelligent retry
│   ├── Dockerfile         # Production-ready container
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # Backend deployment guide
│
└── frontend-vercel/       # Next.js frontend
    ├── app/               # Next.js app directory
    │   ├── page.tsx       # Code editor UI
    │   └── layout.tsx     # Root layout
    ├── .env.example       # Environment variables template
    ├── package.json       # Node dependencies
    └── README.md          # Frontend deployment guide
```

## 🚀 Quick Start

### Prerequisites
- **Backend**: Python 3.11+, Docker, gcc, g++
- **Frontend**: Node.js 18+, npm

### 1. Backend Setup (Local)

```bash
cd compiler-backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Backend runs on: `http://localhost:5000`

### 2. Frontend Setup (Local)

```bash
cd frontend-vercel

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local and set:
# NEXT_PUBLIC_BACKEND_URL=http://localhost:5000

# Start dev server
npm run dev
```

Frontend runs on: `http://localhost:3000`

## 🌐 Deployment

### Deploy Backend on Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Deploy:
```bash
cd compiler-backend
railway login
railway init
railway up
```

3. Your backend URL will be: `https://your-app.railway.app`

**Alternative platforms**: Render, Fly.io (see `/compiler-backend/README.md`)

### Deploy Frontend on Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd frontend-vercel
vercel
```

3. Set environment variable in Vercel dashboard:
   - **Key**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: Your Railway backend URL (e.g., `https://your-app.railway.app`)

4. Redeploy to apply environment variable

Your frontend will be live at: `https://your-project.vercel.app`

## 🔧 Configuration

### Backend Environment Variables
- `PORT`: Server port (default: 5000, auto-set by Railway/Render)

### Frontend Environment Variables
- `NEXT_PUBLIC_BACKEND_URL`: Backend API URL (**required**)
  - Local: `http://localhost:5000`
  - Production: Your Railway/Render URL

## 📖 API Documentation

### `POST /run`

Execute code with intelligent compilation.

**Request:**
```json
{
  "language": "c",
  "code": "#include <stdio.h>\nint main() { printf(\"Hi\"); return 0; }",
  "input": ""
}
```

**Response:**
```json
{
  "stdout": "Hi",
  "stderr": "",
  "error": null,
  "success": true,
  "compilation_info": "✅ Compiled successfully using: C11 standard"
}
```

**Supported Languages:**
- `c`: C language
- `cpp` or `c++`: C++ language
- `python`: Python 3

## 🎯 How It Works

### Intelligent Retry System

When you submit C/C++ code, the backend:

1. **First attempt**: Tries modern standards (C11/C++17) with optimizations
2. **On failure**: Falls back to permissive mode with warnings suppressed
3. **Continues**: Tries older standards (C99, C89, C++14, C++11, C++98)
4. **Final attempt**: Maximum permissive mode with `-fpermissive` flag
5. **Success**: Returns first successful compilation
6. **All fail**: Returns error with AI suggestions

### Example Flow

```
Code submitted → Try C11 -O2
                  ↓ Failed (missing header)
                → Try C11 permissive -w
                  ↓ Failed (implicit declaration)
                → Try GNU C11 -w
                  ✅ SUCCESS!
                → Execute and return output
```

## 🛠️ Tech Stack

### Backend
- **Flask 3.0**: Python web framework
- **gcc/g++**: C/C++ compilers
- **python3**: Python interpreter
- **Docker**: Containerization

### Frontend
- **Next.js 15**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **React 19**: UI library

## 🔒 Security Features

- ✅ Non-root container execution
- ✅ Random temp file names
- ✅ Automatic file cleanup
- ✅ Execution timeouts
- ✅ Output size limits
- ✅ CORS properly configured
- ✅ Input sanitization
- ✅ No shell injection vulnerabilities

## 📝 Example Code

### C Example
```c
#include <stdio.h>
int main() {
    printf("Hello World!\n");
    return 0;
}
```

### C++ Example
```cpp
#include <iostream>
using namespace std;
int main() {
    cout << "Hello World!" << endl;
    return 0;
}
```

### Python Example
```python
print("Hello World!")
```

## 🐛 Troubleshooting

### Backend Issues

**Compilation timeouts:**
- Default timeout is 30s for compilation
- Adjust `TIMEOUT_SECONDS` in `app.py` if needed

**Missing compilers:**
```bash
# Install compilers
sudo apt-get install gcc g++ python3
```

### Frontend Issues

**Backend connection failed:**
- Verify `NEXT_PUBLIC_BACKEND_URL` is set correctly
- Check backend is running and accessible
- Verify CORS is enabled (already configured)

**Build errors:**
```bash
# Clean and rebuild
rm -rf .next node_modules
npm install
npm run build
```

## 📚 Detailed Documentation

- **Backend**: See [`/compiler-backend/README.md`](compiler-backend/README.md)
- **Frontend**: See [`/frontend-vercel/README.md`](frontend-vercel/README.md)

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🎓 Learn More

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Railway Deployment](https://docs.railway.app/)
- [Vercel Deployment](https://vercel.com/docs)

## 🌟 Features Highlights

| Feature | Description |
|---------|-------------|
| **Smart Compilation** | Auto-tries 8-10 different compiler strategies |
| **Zero Warnings** | All warnings automatically suppressed |
| **AI Suggestions** | Helpful hints when compilation fails |
| **Production Ready** | Docker, security hardening, proper error handling |
| **Easy Deployment** | One-click deploy to Railway + Vercel |
| **Modern Stack** | Next.js 15, React 19, TypeScript, Tailwind CSS |

## 💡 Why This Architecture?

**Separation of Concerns:**
- ✅ Frontend (Vercel): Static/serverless, no compilation load
- ✅ Backend (Railway): Dedicated container with compilers
- ✅ Easy to scale independently
- ✅ Frontend stays fast even during heavy compilation

**vs Monolithic Approach:**
- ❌ Can't run compilers on Vercel (no docker support)
- ❌ Would need serverless functions with cold starts
- ❌ Complex deployment and scaling

---

**Made with ❤️ for developers who want a reliable online code runner**
