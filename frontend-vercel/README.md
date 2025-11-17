# Online Code Runner - Frontend

Next.js frontend for the online code runner. Designed to be deployed on Vercel.

## 🚀 Features

- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **TypeScript**: Full type safety
- **Language Support**: C, C++, and Python
- **Real-time Feedback**: See compilation and execution results instantly
- **Smart Backend Integration**: Connects to separate compiler backend service

## 📦 Installation

```bash
npm install
```

## 🛠️ Development

1. Copy the environment example file:
```bash
cp .env.local.example .env.local
```

2. Edit `.env.local` and set your backend URL:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🏗️ Build

```bash
npm run build
```

## 🌐 Deployment on Vercel

### Option 1: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Follow the prompts and set environment variable:
   - `NEXT_PUBLIC_BACKEND_URL`: Your backend URL (e.g., `https://your-backend.railway.app`)

### Option 2: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository
4. Set Root Directory to `frontend-vercel`
5. Add environment variable:
   - **Key**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend.railway.app`)
6. Click "Deploy"

Your frontend will be live at: `https://your-project.vercel.app`

## 🔧 Environment Variables

### `NEXT_PUBLIC_BACKEND_URL` (required)

The URL of your backend compiler service.

- **Local development**: `http://localhost:5000`
- **Production**: Your Railway/Render backend URL
- **Example**: `https://code-runner-backend.railway.app`

## 📝 Project Structure

```
frontend-vercel/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main code runner page
│   └── globals.css         # Global styles
├── public/                 # Static assets
├── .env.local.example      # Environment variables example
├── next.config.ts          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
└── package.json            # Dependencies
```

## 🎨 Tech Stack

- **Next.js 15**: React framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **React 19**: Latest React features

## 🔒 Security Notes

- Backend URL is exposed to the client (as `NEXT_PUBLIC_*` env vars)
- All code execution happens on the backend, not in the browser
- The frontend is a static/serverless deployment with no server-side execution

## 🐛 Troubleshooting

**"Failed to connect to backend" error:**
- Check that `NEXT_PUBLIC_BACKEND_URL` is set correctly
- Verify your backend is running and accessible
- Check CORS is enabled on the backend (already configured in backend code)

**Build errors:**
- Run `npm install` to ensure all dependencies are installed
- Delete `.next` folder and rebuild: `rm -rf .next && npm run build`

**Environment variable not working:**
- Restart the dev server after changing `.env.local`
- For Vercel deployments, redeploy after changing environment variables

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Vercel Deployment Documentation](https://vercel.com/docs)

## 🤝 Backend Integration

This frontend works with the companion backend service in `/compiler-backend`.

The backend must:
- Be deployed on Railway, Render, or similar platform
- Have CORS enabled (already configured)
- Accept POST requests to `/run` endpoint
- Return JSON with `stdout`, `stderr`, `error`, and `success` fields

See `/compiler-backend/README.md` for backend deployment instructions.
