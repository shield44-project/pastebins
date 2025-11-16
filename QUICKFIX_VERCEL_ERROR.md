# Quick Fix: Internal Server Error on Vercel

If you're experiencing "Internal Server Error" when uploading files on Vercel, this has been fixed! 🎉

## ✅ Latest Fix (Critical)

**Problem**: The app was not reading the `CODES_DIRECTORY` environment variable, causing read-only filesystem errors.

**Solution**: Updated `app.py` to read the environment variable. The app now correctly uses `/tmp/stored_codes` on Vercel.

## What Was Fixed

1. **Environment Variable Support**: The application now reads `CODES_DIRECTORY` from environment variables
2. **Error Handling**: Comprehensive error messages instead of generic 500 errors
3. **Vercel Configuration**: Included `vercel.json` automatically configures `/tmp` storage

## What You Need to Know

### For Vercel Deployments

Vercel uses a **serverless environment** with an ephemeral (temporary) filesystem. This means:

1. **Files uploaded won't persist** between function invocations
2. You can only write to `/tmp` directory (up to 500MB, temporary)
3. For production, you need external storage (S3, Vercel Blob, etc.)

### Quick Setup for Vercel

The repository now includes a `vercel.json` configuration file that sets up:
- Flask in production mode (`FLASK_DEBUG=False`)
- Storage directory to `/tmp/stored_codes` (automatically read by the app)

**Just deploy to Vercel** and it should work! However, remember:
- ⚠️ Uploaded files will be **temporary** and won't persist
- ⚠️ Files will be lost when the serverless function terminates

## Error Messages You'll See

Instead of generic errors, you'll now see helpful messages:

### File Too Large
```json
{
  "error": "File too large. Maximum upload size is 16MB.",
  "max_size": "16MB"
}
```
**Solution**: Reduce your file size to under 16MB

### Permission Issues
```json
{
  "error": "Failed to create storage directory. The server may have limited write permissions."
}
```
**Solution**: This is expected on some platforms. On Vercel, the `/tmp` directory should work.

### Invalid Input
```json
{
  "error": "No files selected"
}
```
**Solution**: Make sure you've selected files before clicking upload

### Wrong File Type
```json
{
  "error": "No valid files were uploaded. Errors: test.java: Wrong file extension - expected .py"
}
```
**Solution**: Make sure your file extension matches the selected language

## For Production Use on Vercel

If you need **persistent storage**, you should:

1. **Use Vercel Blob Storage**:
   ```bash
   npm install @vercel/blob
   ```
   Then modify `app.py` to use Vercel Blob instead of file system

2. **Use AWS S3**:
   ```bash
   pip install boto3
   ```
   Configure S3 credentials and modify file operations

3. **Use a Database**:
   Store file content and metadata in a database

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed instructions.

## Testing Locally

To test the error handling locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest test_upload_error_handling.py -v

# Run the application
python app.py
```

## More Information

- **Detailed Fix Summary**: [FIX_INTERNAL_SERVER_ERROR.md](FIX_INTERNAL_SERVER_ERROR.md)
- **Vercel Deployment Guide**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- **General Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

## Summary

✅ **Error handling is now comprehensive**
✅ **Clear error messages guide you to solutions**
✅ **Vercel configuration is included**
✅ **All tests pass**
✅ **No security vulnerabilities**

The internal server error issue is resolved. You'll now get helpful error messages that tell you exactly what went wrong and how to fix it! 🎉
