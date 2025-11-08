# Netlify Deployment Guide

This project is configured for easy deployment on Netlify as a static site with client-side functionality.

## Features Available on Netlify

✅ **Fully Functional Static Site**
- Interactive code upload and storage using browser localStorage
- Code viewer with syntax highlighting
- Responsive design for all devices
- File management (upload, view, delete)
- Drag-and-drop file upload
- Support for multiple programming languages

✅ **Encrypted File Viewer**
- Displays encrypted Python files
- Note: Decryption requires a separate backend server

## Quick Deploy to Netlify

### Option 1: Deploy via Netlify Dashboard

1. **Fork or clone this repository**
2. **Login to Netlify** at https://netlify.com
3. **Click "Add new site"** → "Import an existing project"
4. **Connect your Git repository** (GitHub, GitLab, or Bitbucket)
5. **Configure build settings:**
   - Build command: (leave empty)
   - Publish directory: `.` (root)
6. **Click "Deploy site"**

Your site will be live at: `https://[random-name].netlify.app`

### Option 2: Deploy via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from the repository root
netlify deploy --prod
```

### Option 3: Deploy via Drag and Drop

1. Go to https://app.netlify.com/drop
2. Drag the entire project folder to the drop zone
3. Your site will be deployed instantly!

## Configuration

The repository includes a `netlify.toml` file with optimal settings:

```toml
[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Custom Domain Setup

1. In Netlify dashboard, go to **Site settings** → **Domain management**
2. Click **Add custom domain**
3. Follow the instructions to configure your DNS

## Environment Variables

No environment variables are required for the static site deployment.

## File Storage

The static site uses browser localStorage to store uploaded code files. This means:
- Files are stored locally in the user's browser
- Files persist across browser sessions
- Files are private to each user
- No backend database required

## Limitations of Static Deployment

❌ **Features that require a backend (not available on static Netlify):**
- Server-side code execution (Python, Java, C, C++)
- Encrypted file decryption (requires separate backend)
- Multi-user file sharing
- Server-side file storage

To use these features, deploy the Flask backend separately on:
- Heroku
- Railway
- Render
- DigitalOcean
- AWS/Azure/GCP

## Encrypted File Viewer

The encrypted file viewer can display the list of encrypted files but requires a separate decryption server to decrypt them.

To set up decryption:
1. Deploy `decrypt_server.py` on a server (Heroku, Railway, etc.)
2. Update the API endpoint in `viewer.html` if needed
3. Ensure CORS is configured properly

## Testing Locally

To test the static site locally:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

Then visit: http://localhost:8000

## Continuous Deployment

Netlify automatically deploys your site when you push to your Git repository:

1. Push changes to your repository
2. Netlify automatically builds and deploys
3. Your site is updated within seconds

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Open an issue on GitHub
- Contact: shield44-project

## License

MIT License - See LICENSE file for details
