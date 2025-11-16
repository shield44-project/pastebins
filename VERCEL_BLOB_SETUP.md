# Vercel Blob Storage Setup Guide

This guide explains how to integrate Vercel Blob Storage with your Pastebins application for persistent file storage on serverless platforms.

## Overview

Vercel Blob Storage provides persistent, scalable storage for your code files when deploying to serverless platforms like Vercel, where the local filesystem is ephemeral. With Blob storage integration:

- ✅ Files persist across deployments
- ✅ Automatic synchronization between local and blob storage
- ✅ Graceful fallback to local storage if blob storage is unavailable
- ✅ No code changes required in the UI
- ✅ Works alongside GitHub integration

## Prerequisites

1. A Vercel account
2. A Vercel Blob Store created in your project
3. The `BLOB_READ_WRITE_TOKEN` from your Vercel Blob Store

## Step 1: Create a Vercel Blob Store

### Using Vercel Dashboard

1. Go to your Vercel project dashboard
2. Navigate to the **Storage** tab
3. Click **Create Database** or **Add Store**
4. Select **Blob Store**
5. Give it a name (e.g., `pastebins-storage`)
6. Click **Create**

### Using Vercel CLI

```bash
vercel blob create pastebins-storage
```

## Step 2: Get Your Read-Write Token

After creating the blob store:

1. In the Vercel dashboard, go to your blob store
2. Navigate to the **Settings** or **Tokens** tab
3. Find the **Read-Write Token**
4. Copy the token (it will look like: `vercel_blob_rw_xxxxxxxxxxxxx`)

**Important:** Keep this token secure. It provides full read and write access to your blob storage.

## Step 3: Configure Environment Variable

### For Vercel Deployment

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add a new variable:
   - **Name:** `BLOB_READ_WRITE_TOKEN`
   - **Value:** Your blob read-write token (e.g., `vercel_blob_rw_GmsSyO1ENI6nA5GJ_ETd7tIhY7RialiPNyz5YaP8U2EZTAZ`)
   - **Environment:** Select **Production**, **Preview**, and **Development**
4. Click **Save**
5. Redeploy your application

### For Local Development

Add to your `.env` file:

```bash
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_YOUR_TOKEN_HERE
```

Or export as an environment variable:

```bash
export BLOB_READ_WRITE_TOKEN=vercel_blob_rw_YOUR_TOKEN_HERE
```

## Step 4: Verify Integration

After deploying with the `BLOB_READ_WRITE_TOKEN` environment variable:

1. Upload a new code file through the web interface
2. Check your application logs for confirmation:
   ```
   Vercel Blob Storage enabled
   File uploaded to blob storage: stored_codes/python/hello.py
   ```
3. View the uploaded file to confirm it loads correctly
4. Try editing and deleting to test all operations

## How It Works

### Upload Flow

1. User uploads a file via the web interface
2. File is saved to local filesystem (for immediate access)
3. File is automatically uploaded to Vercel Blob storage (for persistence)
4. Blob URL is stored in metadata
5. File is also committed to GitHub (if configured)

### Read Flow

1. User requests to view a file
2. System attempts to fetch from Blob storage first (using blob_url in metadata)
3. If Blob fetch fails, falls back to local filesystem
4. Content is displayed to user

### Edit Flow

1. User edits a file
2. Old blob is deleted (if it exists)
3. New content is saved to local filesystem
4. New content is uploaded to Blob storage
5. Metadata is updated with new blob_url
6. Changes are committed to GitHub (if configured)

### Delete Flow

1. User deletes a file
2. File is deleted from Blob storage (if blob_url exists)
3. File is deleted from local filesystem
4. Metadata is updated
5. Changes are committed to GitHub (if configured)

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      Flask Application          │
│  ┌──────────────────────────┐  │
│  │  Blob Storage Module     │  │
│  │  (blob_storage.py)       │  │
│  └──────────────────────────┘  │
│           │                     │
│           ▼                     │
│  ┌──────────────┐  ┌─────────┐ │
│  │Local Storage │  │ GitHub  │ │
│  └──────────────┘  └─────────┘ │
└───────────┬─────────────────────┘
            │
            ▼
  ┌──────────────────────┐
  │  Vercel Blob API     │
  │  blob.vercel-storage.com │
  └──────────────────────┘
```

## API Reference

The blob storage module (`blob_storage.py`) provides:

### VercelBlobStorage Class

```python
blob_client = VercelBlobStorage(token=BLOB_READ_WRITE_TOKEN)
```

#### Methods

**put(pathname, content, content_type='text/plain')**
- Upload a file to blob storage
- Returns: Dict with 'url', 'downloadUrl', 'pathname', etc.

**get(url)**
- Download a file from blob storage
- Returns: File content as string

**delete(url)**
- Delete a file from blob storage
- Returns: True if successful

**list_blobs(prefix=None)**
- List all blobs, optionally filtered by prefix
- Returns: List of blob metadata dictionaries

### Helper Functions

**get_blob_client()**
- Get a configured blob client instance
- Returns: VercelBlobStorage instance or None

**is_blob_storage_enabled()**
- Check if blob storage is configured
- Returns: True/False

## Troubleshooting

### Issue: "Blob storage not enabled - token not configured"

**Solution:** Ensure `BLOB_READ_WRITE_TOKEN` environment variable is set correctly and redeploy.

### Issue: "Failed to upload to blob storage: 401"

**Solution:** Your token is invalid or expired. Generate a new token from Vercel dashboard.

### Issue: "Failed to upload to blob storage: Network error"

**Solution:** 
- Check your internet connection
- Verify Vercel Blob API is accessible
- The application will continue to work with local storage only

### Issue: Files not persisting after deployment

**Solution:**
- Verify blob storage integration is working (check logs)
- Ensure environment variable is set in Vercel
- Redeploy after setting the environment variable

## Cost Considerations

Vercel Blob Storage pricing (as of 2025):

- **Free tier:** 1 GB storage, 1 GB bandwidth per month
- **Pro:** $0.15/GB storage, $0.30/GB bandwidth
- **Enterprise:** Custom pricing

For a typical code storage application:
- ~1000 files × 10 KB each = ~10 MB storage
- Well within free tier for most use cases

## Security

- ✅ Tokens are stored as environment variables (not in code)
- ✅ All blob URLs are public (files are intentionally shared)
- ✅ File uploads are validated and sanitized
- ✅ No direct file system access from users
- ⚠️ Keep your `BLOB_READ_WRITE_TOKEN` secure - it provides full access to your blob storage

## Migration from GitHub-only Storage

If you're currently using GitHub as your only storage backend:

1. Enable blob storage by setting `BLOB_READ_WRITE_TOKEN`
2. Existing files will continue to work from local filesystem
3. New uploads will be stored in both local and blob storage
4. Optionally, re-upload existing files through the UI to add them to blob storage

## Disabling Blob Storage

To disable blob storage and revert to local-only storage:

1. Remove the `BLOB_READ_WRITE_TOKEN` environment variable
2. Redeploy your application
3. Application will fall back to local filesystem only

## Support

For issues or questions:
- Check application logs for detailed error messages
- Review [Vercel Blob documentation](https://vercel.com/docs/storage/vercel-blob)
- Open an issue on GitHub
