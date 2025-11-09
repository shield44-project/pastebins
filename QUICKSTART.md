# Quick Start Guide - TypeScript and React Development

This guide will get you up and running with the TypeScript/React frontend in under 5 minutes.

## Prerequisites

- Node.js 18 or higher installed
- npm (comes with Node.js)
- A code editor (VS Code recommended)

## Installation

1. **Clone the repository** (if you haven't already):
```bash
git clone https://github.com/shield44-project/pastebins.git
cd pastebins
```

2. **Install dependencies**:
```bash
npm install
```

This will install all required packages including React, TypeScript, and Webpack.

## Development

### Start the Development Server

```bash
npm start
```

This will:
- Start the webpack dev server on http://localhost:3000
- Open your default browser automatically
- Enable hot module replacement (changes reflect instantly)

Alternative command (doesn't auto-open browser):
```bash
npm run dev
```

### Making Changes

1. **Edit any file in the `src/` directory**
2. **Save the file**
3. **See changes instantly in your browser** (hot reload)

### File Structure

```
src/
├── components/       # React components
├── types/           # TypeScript type definitions
├── utils/           # Utility functions
├── services/        # API services
├── App.tsx          # Main app component
├── index.tsx        # Entry point
└── styles.css       # Global styles
```

## Building for Production

### Create Production Build

```bash
npm run build
```

This creates optimized files in the `dist/` directory:
- Minified JavaScript
- Code splitting (vendors separate from app code)
- Optimized HTML
- Ready for deployment

### Build Output

```
dist/
├── bundle.[hash].js      # Main application code (~13KB)
├── bundle.[hash].js      # Vendor code (React, etc.) (~189KB)
└── index.html           # Entry HTML file
```

## Common Tasks

### Add a New Component

1. Create a new file in `src/components/`:
```typescript
// src/components/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
}

const MyComponent: React.FC<MyComponentProps> = ({ title }) => {
  return <div>{title}</div>;
};

export default MyComponent;
```

2. Import it in `App.tsx`:
```typescript
import MyComponent from './components/MyComponent';
```

3. Use it:
```typescript
<MyComponent title="Hello World" />
```

### Add a New Utility Function

1. Edit `src/utils/helpers.ts`:
```typescript
export const myHelper = (input: string): string => {
  return input.toUpperCase();
};
```

2. Import and use:
```typescript
import { myHelper } from './utils';
const result = myHelper('hello'); // 'HELLO'
```

### Add New Types

1. Edit `src/types/index.ts`:
```typescript
export interface MyType {
  id: string;
  name: string;
}
```

2. Import and use:
```typescript
import { MyType } from './types';
const obj: MyType = { id: '1', name: 'Test' };
```

## Troubleshooting

### Port 3000 Already in Use

Use a different port:
```bash
npm run dev -- --port 3001
```

### Build Errors

1. Delete node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

2. Clear build cache:
```bash
rm -rf dist
npm run build
```

### TypeScript Errors

Make sure all dependencies have types installed:
```bash
npm install --save-dev @types/package-name
```

### Changes Not Reflecting

1. Hard refresh your browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. Restart the dev server: `Ctrl+C` then `npm start`
3. Clear browser cache

## Integration with Flask Backend

### Development Setup (Recommended)

1. **Terminal 1 - Start Flask backend**:
```bash
python app.py
# Backend runs on http://localhost:5000
```

2. **Terminal 2 - Start React frontend**:
```bash
npm start
# Frontend runs on http://localhost:3000
```

3. **Configure CORS** in Flask app to allow requests from localhost:3000

4. **Make API calls** from React components using the API service in `src/services/api.ts`

### Production Setup

1. **Build the React app**:
```bash
npm run build
```

2. **Configure Flask to serve the `dist/` directory**:
```python
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='dist')

@app.route('/')
def index():
    return send_from_directory('dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('dist', path)
```

3. **Run Flask**: Single server serves both frontend and API

## Next Steps

1. ✅ Read [TYPESCRIPT_REACT_SETUP.md](TYPESCRIPT_REACT_SETUP.md) for detailed documentation
2. ✅ Explore the example components in `src/components/`
3. ✅ Check out modern JavaScript examples in `src/examples/`
4. ✅ Review the type definitions in `src/types/`
5. ✅ Try modifying components and see changes in real-time

## Getting Help

- **Documentation**: See [TYPESCRIPT_REACT_SETUP.md](TYPESCRIPT_REACT_SETUP.md)
- **Examples**: Check `src/examples/modern-javascript.js`
- **Issues**: Open an issue on GitHub
- **React Docs**: https://react.dev/
- **TypeScript Docs**: https://www.typescriptlang.org/docs/

## Useful Commands Reference

| Command | Description |
|---------|-------------|
| `npm install` | Install all dependencies |
| `npm start` | Start dev server (auto-opens browser) |
| `npm run dev` | Start dev server (no auto-open) |
| `npm run build` | Create production build |
| `npm run build:dev` | Create development build |
| `npm audit` | Check for security vulnerabilities |
| `npm update` | Update dependencies |

## Tips

- 💡 Use TypeScript's type inference - let the compiler help you
- 💡 Install the React Developer Tools browser extension
- 💡 Use VS Code with TypeScript extensions for best experience
- 💡 Check the browser console for errors during development
- 💡 Use `console.log()` for debugging, remove before production
- 💡 Build frequently to catch errors early

---

**Happy Coding! 🚀**
