# Vercel Deployment Guide

This guide explains how to deploy the application to Vercel and the limitations you should be aware of.

## ✅ Quick Fix Applied

The application now correctly reads the `CODES_DIRECTORY` environment variable. The included `vercel.json` configuration sets this to `/tmp/stored_codes` automatically.

## Important Notes About Vercel Deployment

### Serverless Environment Limitations

Vercel uses a **serverless architecture** which has the following characteristics:

1. **Ephemeral Filesystem**: Files uploaded during a request are stored temporarily and may not persist between requests
2. **Read-only in some directories**: The `/var/task` directory (where your code lives) is read-only
3. **Timeout limits**: Serverless functions have execution time limits (typically 10-60 seconds)
4. **No persistent storage**: Without external storage (S3, database, etc.), uploaded files won't persist

### Recommended Solutions for File Storage on Vercel

For production deployment on Vercel, you should:

1. **Use Object Storage**:
   - AWS S3
   - Cloudflare R2
   - Vercel Blob Storage
   - Any S3-compatible storage service

2. **Use a Database**:
   - Store file metadata in a database
   - Store file content in a database or object storage

3. **Use Vercel's `/tmp` Directory** (Default Configuration):
   - The included `vercel.json` automatically configures this
   - Files can be written to `/tmp` directory (up to 500MB)
   - Files in `/tmp` are ephemeral and only exist for the duration of the function execution
   - Not suitable for long-term storage but prevents read-only filesystem errors

## Error Handling Improvements

This application has been updated with comprehensive error handling that provides:

- **User-friendly error messages** instead of generic "Internal Server Error"
- **Specific error details** for permission issues, file system errors, etc.
- **Server-side logging** to help diagnose issues on Vercel
- **Graceful degradation** when operations fail

## Configuration for Vercel

### Automatic Configuration (Recommended)

The repository includes a `vercel.json` file that automatically configures the application for Vercel:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_DEBUG": "False",
    "CODES_DIRECTORY": "/tmp/stored_codes"
  }
}
```

The app reads the `CODES_DIRECTORY` environment variable, so you can override it in Vercel's dashboard if needed.

**Note**: Files in `/tmp` are not persistent and will be lost between function invocations.

### Option 2: Use External Storage (Recommended)

Modify `app.py` to use cloud storage:

```python
# Example using boto3 for S3
import boto3
s3_client = boto3.client('s3')

# Replace file save operations with S3 uploads
s3_client.put_object(
    Bucket='your-bucket',
    Key=f'codes/{filename}',
    Body=file_content
)
```

## Testing on Vercel

After deployment, you can test the error handling by:

1. **Uploading a file** - Check if you get a clear error message about storage limitations
2. **Uploading a large file (>16MB)** - Should get "File too large" error
3. **Invalid file types** - Should get specific validation errors

## Alternative Platforms

If persistent file storage is required without additional infrastructure, consider these platforms:

- **Heroku** - Has a persistent filesystem (with limitations)
- **Railway** - Provides persistent storage
- **Render** - Offers persistent disks
- **DigitalOcean App Platform** - Has persistent storage options
- **Traditional VPS** - Full control over storage

## Common Errors and Solutions

### "Failed to create storage directory"
**Cause**: Trying to write to a read-only directory on Vercel
**Solution**: Configure `CODES_DIRECTORY` to `/tmp/stored_codes` or use external storage

### "Permission denied - cannot write file"
**Cause**: Attempting to write to a protected directory
**Solution**: Use `/tmp` directory or external storage service

### "An unexpected error occurred during file upload"
**Cause**: Various issues - check server logs for details
**Solution**: Review Vercel function logs to see the actual error message logged by the application

## Getting More Information

When errors occur, the application now:
1. Logs detailed error information server-side
2. Returns user-friendly error messages to the client
3. Includes specific error codes (400, 413, 500) for different scenarios

Check your Vercel deployment logs to see the full error details and stack traces for debugging.
