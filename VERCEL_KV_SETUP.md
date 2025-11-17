# Redis/KV Setup Guide for Notes Storage

This guide explains how to set up Redis-compatible storage for persistent notes storage in your Pastebins application.

## Overview

The application supports multiple Redis providers for notes storage:

- ✅ **Vercel KV** (Recommended for Vercel deployments)
- ✅ **Redis Labs** (External Redis service)
- ✅ **Upstash Redis** (Serverless Redis)
- ✅ **Any Redis-compatible database**
- ✅ Graceful fallback to local storage if Redis is unavailable

## Option 1: Vercel KV (Recommended for Vercel)

### Prerequisites

1. A Vercel account
2. A Vercel KV database created in your project

### Step 1: Create a Vercel KV Database

#### Using Vercel Dashboard

1. Go to your Vercel project dashboard
2. Navigate to the **Storage** tab
3. Click **Create Database**
4. Select **KV** (Key-Value Store)
5. Give it a name (e.g., `pastebins-kv`)
6. Click **Create**

#### Using Vercel CLI

```bash
vercel kv create pastebins-kv
```

### Step 2: Get Your KV Credentials

After creating the KV database:

1. In the Vercel dashboard, go to your KV database
2. Navigate to the **.env.local** tab
3. Copy the environment variables shown:
   - `KV_REST_API_URL`
   - `KV_REST_API_TOKEN`

### Step 3: Configure Environment Variables

#### For Vercel Deployment

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add the following variables:
   
   **Variable 1:**
   - **Name:** `KV_REST_API_URL`
   - **Value:** Your KV REST API URL (e.g., `https://your-kv-db.kv.vercel-storage.com`)
   - **Environment:** Select **Production**, **Preview**, and **Development**
   
   **Variable 2:**
   - **Name:** `KV_REST_API_TOKEN`
   - **Value:** Your KV REST API token
   - **Environment:** Select **Production**, **Preview**, and **Development**

4. Click **Save**
5. Redeploy your application

#### For Local Development

Add to your `.env` file or export as environment variables:

```bash
export KV_REST_API_URL=https://your-kv-db.kv.vercel-storage.com
export KV_REST_API_TOKEN=your_token_here
```

## Option 2: External Redis Service (Redis Labs, Upstash, etc.)

If you prefer using an external Redis provider instead of Vercel KV:

### Step 1: Get Redis Connection URL

From your Redis provider (e.g., Redis Labs, Upstash, Railway):

1. Create a new Redis database
2. Copy the **Redis URL** (format: `redis://username:password@host:port`)

Example from Redis Labs:
```
redis://default:UeX2zubkNkTUjD5xLCUCbCn0zf3QRR1V@redis-15784.c98.us-east-1-4.ec2.cloud.redislabs.com:15784
```

### Step 2: Configure Environment Variable

#### For Vercel Deployment

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add one of these variables:
   
   **Option A: `KV_REST_API_REDIS_URL`** (Recommended)
   - **Name:** `KV_REST_API_REDIS_URL`
   - **Value:** Your full Redis URL
   - **Environment:** Select **Production**, **Preview**, and **Development**
   
   **Option B: `REDIS_URL`** (Alternative)
   - **Name:** `REDIS_URL`
   - **Value:** Your full Redis URL
   - **Environment:** Select **Production**, **Preview**, and **Development**

4. Click **Save**
5. Redeploy your application

#### For Local Development

```bash
export KV_REST_API_REDIS_URL=redis://default:password@host:port
# OR
export REDIS_URL=redis://default:password@host:port
```

## Step 4: Verify Integration

After deploying with Redis/KV credentials:

1. Open your application
2. Navigate to any code file page
3. Click the **"📝 Notes"** button
4. You should see: "✅ Using Redis storage (server-side)" or "✅ Using Vercel KV storage (server-side)"
5. Create a test note with a screenshot
6. Refresh the page - the note should persist

## Features

### Notes API

The application provides a RESTful API for notes:

- **GET `/api/notes`** - List all notes (summary only)
- **POST `/api/notes`** - Create a new note
- **GET `/api/notes/<note_id>`** - Get a specific note with full data
- **PUT `/api/notes/<note_id>`** - Update a note
- **DELETE `/api/notes/<note_id>`** - Delete a note

### Notes Structure

Each note contains:

```json
{
  "id": "1234567890",
  "title": "Note Title",
  "content": "Note content...",
  "images": [
    {
      "name": "screenshot.png",
      "dataUrl": "data:image/png;base64,..."
    }
  ],
  "created": 1234567890.123,
  "modified": 1234567890.456
}
```

### Storage Details

- **Notes** are stored as JSON in Redis with key `note:{note_id}`
- **Note IDs list** is stored in a Redis set with key `notes:all`
- **Images** are stored as base64-encoded data URLs within the note JSON
- **Automatic fallback** to in-memory storage if KV is unavailable

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
│  │  Notes Storage Module    │  │
│  │  (notes_storage.py)      │  │
│  └──────────────────────────┘  │
│           │                     │
│           ▼                     │
│  ┌──────────────┐  ┌─────────┐ │
│  │ Local Memory │  │ Redis   │ │
│  │  (fallback)  │  │ Client  │ │
│  └──────────────┘  └─────────┘ │
└───────────┬─────────────────────┘
            │
            ▼
  ┌──────────────────────┐
  │  Vercel KV (Redis)   │
  │  KV Storage          │
  └──────────────────────┘
```

## Security Considerations

- ✅ All data is stored server-side (not exposed to client)
- ✅ API endpoints validate input data
- ✅ Image data is validated before storage
- ✅ Note IDs are timestamped and unique
- ⚠️ Keep your `KV_REST_API_TOKEN` secure - it provides full access to your KV database
- ⚠️ Consider implementing authentication for production use

## Cost Considerations

Vercel KV pricing (as of 2025):

- **Free tier:** 30 MB storage, 3,000 commands per month
- **Pro:** $0.10/100K commands + $0.30/GB storage
- **Enterprise:** Custom pricing

For typical notes usage:
- ~100 notes × 50 KB each (with images) = ~5 MB storage
- ~1000 reads/writes per day = ~30K commands per month
- Well within free tier for most use cases

## Image Storage Considerations

### Current Implementation

Images are stored as base64-encoded data URLs within note JSON:

**Pros:**
- Simple implementation
- No separate file storage needed
- Atomic operations

**Cons:**
- Larger storage size (~33% overhead from base64 encoding)
- Network transfer overhead

### Recommended for Large-Scale Usage

For applications with many images, consider:

1. **Vercel Blob Storage** for images:
   ```python
   # Store images in Blob
   blob_url = blob_client.put(image_data, f"notes/{note_id}/{image_name}")
   
   # Store only URL in KV
   note_data['images'] = [{'name': name, 'url': blob_url}]
   ```

2. **Image optimization**:
   - Resize images before upload
   - Compress images (JPEG quality 80-90%)
   - Limit image dimensions (e.g., max 1920x1080)

## Troubleshooting

### Issue: "Using local storage (will reset on refresh)"

**Solution:** KV credentials are not configured. Set `KV_REST_API_URL` and `KV_REST_API_TOKEN` environment variables.

### Issue: "Failed to connect to Vercel KV"

**Solution:** 
- Verify your KV database is created
- Check that environment variables are set correctly
- Ensure the KV database is in the same region/organization
- The application will fall back to local storage

### Issue: Notes not persisting

**Solution:**
- Check application logs for KV connection errors
- Verify environment variables are set in Vercel dashboard
- Redeploy after setting environment variables

### Issue: "redis module not found"

**Solution:** Install the redis Python package:
```bash
pip install redis>=5.0.0
```

## Migration

### From localStorage to Vercel KV

If users have notes in localStorage (from the static index.html):

1. Notes in localStorage cannot be automatically migrated to KV
2. Users can manually recreate important notes
3. Consider adding an import/export feature

### Backup and Restore

To backup notes:

```python
from notes_storage import get_notes_storage

storage = get_notes_storage()
notes = storage.list_notes()

# Get full data for each note
backup = []
for note_summary in notes:
    full_note = storage.get_note(note_summary['id'])
    backup.append(full_note)

# Save to file
import json
with open('notes_backup.json', 'w') as f:
    json.dump(backup, f)
```

## Disabling KV Storage

To disable KV and use local memory only:

1. Remove `KV_REST_API_URL` and `KV_REST_API_TOKEN` environment variables
2. Redeploy your application
3. Notes will be stored in memory (lost on restart)

## Support

For issues or questions:
- Check application logs for detailed error messages
- Review [Vercel KV documentation](https://vercel.com/docs/storage/vercel-kv)
- Open an issue on GitHub

## Future Enhancements

- [ ] Note search functionality
- [ ] Note categories/tags
- [ ] Markdown support in note content
- [ ] Note sharing via links
- [ ] Export notes to PDF
- [ ] Image optimization (resize, compress)
- [ ] Migration tool from localStorage
