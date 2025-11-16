# Quick Fix: Internal Server Error on Vercel

If you're experiencing "Internal Server Error" when uploading files on Vercel, this has been fixed! 🎉

## ✅ Latest Update: GitHub Integration

**NEW**: Files uploaded via the website can now be automatically committed to your GitHub repository!

This solves the ephemeral filesystem problem on Vercel - uploaded files are now permanently stored in your GitHub repo.

### Setup GitHub Integration (Recommended)

1. Create a GitHub Personal Access Token (with `repo` scope)
2. Add it to Vercel environment variables as `GITHUB_TOKEN`
3. Files uploaded via website will auto-commit to your repo

See [GITHUB_INTEGRATION_SETUP.md](GITHUB_INTEGRATION_SETUP.md) for detailed setup instructions.

## ✅ Previous Fix: Environment Variable Support

**Problem**: The app was not reading the `CODES_DIRECTORY` environment variable, causing read-only filesystem errors.

**Solution**: Updated `app.py` to read the environment variable. The app now correctly uses `/tmp/stored_codes` on Vercel.

---

## How File Upload Works Now

### With GitHub Integration (Recommended):
1. File is uploaded via website
2. Saved locally to `/tmp/stored_codes/`
3. **Automatically committed to GitHub repository** ← NEW!
4. Files persist permanently across deployments ✅

### Without GitHub Integration:
1. File is uploaded via website
2. Saved locally to `/tmp/stored_codes/`
3. Files are temporary - lost on function restart ⚠️

---

## Error Messages

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
**Solution**: This shouldn't happen anymore with the env variable fix. If it does, check your Vercel configuration.

### Invalid Input
```json
{
  "error": "No files selected"
}
```
**Solution**: Make sure you've selected files before clicking upload

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
