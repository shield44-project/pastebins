# Vercel Deployment Guide for NeonBin

This guide explains how to deploy NeonBin to Vercel.

## Prerequisites

- A Vercel account (sign up at https://vercel.com)
- Git repository connected to Vercel

## Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/shield44-project/pastebins)

## Manual Deployment Steps

### 1. Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### 2. Deploy to Vercel

#### Option A: Using Vercel Dashboard

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect the `vercel.json` configuration
5. Click "Deploy"

#### Option B: Using Vercel CLI

```bash
# Login to Vercel
vercel login

# Deploy
vercel
```

### 3. Environment Variables (if needed)

If you need to set environment variables:

1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add any required variables

## Configuration

The `vercel.json` file is already configured with:

- **Build**: Python runtime with Flask app
- **Routes**: Static file serving and API routing
- **Environment**: Production mode

## File Structure

```
pastebins/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── app.py                # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── static/               # Static assets (CSS, JS)
├── templates/            # HTML templates
└── stored_codes/         # Code storage directory
```

## Important Notes

### Storage Limitations

⚠️ **Vercel has read-only filesystem in serverless functions!**

This means:
- **File uploads won't persist** between requests
- **stored_codes/** directory is temporary
- Consider using:
  - **Vercel Blob Storage** for file uploads
  - **Database** (PostgreSQL, MongoDB) for metadata
  - **External storage** (AWS S3, Cloudflare R2)

### Recommended Modifications for Production

For a production deployment on Vercel, you should:

1. **Use a Database for Metadata**
   - Replace JSON file storage with PostgreSQL/MongoDB
   - Store metadata in a persistent database

2. **Use Object Storage for Files**
   - Use Vercel Blob, AWS S3, or Cloudflare R2
   - Store uploaded code files in object storage

3. **Update app.py**
   - Modify file upload handlers to use blob storage
   - Update metadata functions to use database

### Alternative: Use Vercel for Frontend Only

Another option is to:
- Deploy the frontend (HTML/CSS/JS) to Vercel
- Deploy the Flask backend to a different platform:
  - Railway.app
  - Render.com
  - Heroku
  - DigitalOcean App Platform

## Troubleshooting

### Build Fails

- Check `requirements.txt` for all dependencies
- Verify Python version compatibility
- Check build logs in Vercel dashboard

### Routes Not Working

- Verify `vercel.json` routing configuration
- Check that `api/index.py` imports `app` correctly

### Static Files Not Loading

- Ensure static files are in the `static/` directory
- Check that routes in `vercel.json` point to correct paths

## Support

For issues specific to Vercel deployment, check:
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)

## Local Testing

To test the Vercel configuration locally:

```bash
# Install Vercel CLI
npm install -g vercel

# Run in development mode
vercel dev
```

This will simulate the Vercel environment locally.
