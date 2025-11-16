# GitHub Integration Setup Guide

This guide explains how to configure the application to commit uploaded files directly to the GitHub repository.

## What This Does

When enabled, the application will:
1. Save uploaded files locally (for immediate viewing)
2. **Automatically commit and push files to your GitHub repository**
3. Keep the `stored_codes` directory in your repo in sync with uploads

This ensures uploaded files persist across deployments on platforms like Vercel.

## Setup Instructions

### Step 1: Create a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Or visit: https://github.com/settings/tokens

2. Click "Generate new token" → "Generate new token (classic)"

3. Configure the token:
   - **Note**: "Pastebins Web Upload"
   - **Expiration**: Choose your preference (90 days, 1 year, or no expiration)
   - **Scopes**: Select `repo` (Full control of private repositories)
     - This gives access to commit to your repository

4. Click "Generate token"

5. **Copy the token immediately** (you won't be able to see it again!)

### Step 2: Configure Environment Variable

#### For Vercel Deployment:

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add a new environment variable:
   - **Name**: `GITHUB_TOKEN`
   - **Value**: Paste your GitHub personal access token
   - **Environment**: Production, Preview, and Development (check all)
4. Click "Save"

5. Redeploy your application:
   ```bash
   vercel --prod
   ```

#### For Local Development:

Add to your environment or create a `.env` file:

```bash
export GITHUB_TOKEN="your_personal_access_token_here"
export GITHUB_REPO="shield44-project/pastebins"
export GITHUB_BRANCH="main"
```

**Important**: Never commit your `.env` file or token to git!

### Step 3: Verify Configuration

The application will automatically use GitHub integration if:
- ✅ PyGithub is installed (`pip install PyGithub>=2.1.1`)
- ✅ `GITHUB_TOKEN` environment variable is set
- ✅ Token has `repo` permissions

Check the application logs for messages like:
```
Successfully committed to GitHub: stored_codes/python/example.py
Committed metadata to GitHub for python
```

## How It Works

### When You Upload via Website:

1. **File is saved locally** in `/tmp/stored_codes/` (on Vercel) or `stored_codes/` (locally)
2. **File is committed to GitHub** in `stored_codes/{language}/{filename}`
3. **Metadata is committed to GitHub** in `stored_codes/{language}_metadata.json`

### Example Flow:

```
User uploads "hello.py" via website
    ↓
Saved to /tmp/stored_codes/python/hello.py (temporary)
    ↓
Committed to GitHub: stored_codes/python/hello.py (permanent)
    ↓
Updated GitHub: stored_codes/python_metadata.json
    ↓
Files now persist and sync across all deployments
```

## Benefits

### ✅ Persistent Storage
- Files don't disappear after Vercel function restarts
- All uploads are permanently stored in your GitHub repo

### ✅ Version Control
- Every upload is a git commit
- You can see history and revert if needed
- Commit messages show what was uploaded and when

### ✅ No External Storage Needed
- Don't need AWS S3, Vercel Blob, or database
- Your GitHub repo is the storage backend

### ✅ Works Across Deployments
- Files uploaded on one deployment are available on the next
- Consistent experience for users

## Security Considerations

### Token Security

⚠️ **Never commit your GitHub token to the repository!**

- Store token in environment variables only
- Use Vercel's environment variable feature
- Add `.env` to `.gitignore`

### Token Permissions

The token needs `repo` scope to:
- Read repository contents
- Create and update files
- Make commits

This is the minimum permission needed for the integration to work.

### Token Rotation

For security best practices:
- Rotate tokens every 90 days
- Update the `GITHUB_TOKEN` environment variable in Vercel
- Delete old tokens from GitHub settings

## Fallback Behavior

If GitHub integration is **not configured**:
- ✅ File uploads still work (saved locally)
- ⚠️ Files are temporary on Vercel (lost on restart)
- ℹ️ Warning logged: "GitHub integration not configured"

The app gracefully degrades - uploads work either way!

## Troubleshooting

### "GitHub integration not configured"

**Solution**: Set the `GITHUB_TOKEN` environment variable

### "Failed to commit to GitHub"

**Possible causes**:
1. Invalid or expired token → Generate a new token
2. Insufficient permissions → Token needs `repo` scope
3. Branch doesn't exist → Create the branch or check `GITHUB_BRANCH` variable
4. Rate limiting → GitHub API has rate limits, wait and retry

### Files upload but don't appear in GitHub

**Check**:
1. View Vercel function logs for GitHub errors
2. Verify token is set correctly
3. Ensure token hasn't expired
4. Check repository name in `GITHUB_REPO` variable

### "Resource not accessible by integration"

**Solution**: Token needs `repo` scope, not just `public_repo`

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes* | None | Personal access token with `repo` scope |
| `GITHUB_REPO` | No | `shield44-project/pastebins` | Repository in format `owner/repo` |
| `GITHUB_BRANCH` | No | `main` | Branch to commit to |

*Required for GitHub integration to work, but app functions without it

## Testing

### Test Locally:

1. Set environment variables:
   ```bash
   export GITHUB_TOKEN="your_token"
   export GITHUB_REPO="shield44-project/pastebins"
   export GITHUB_BRANCH="main"
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Upload a test file via the web interface

4. Check your GitHub repository:
   - New commit should appear
   - File should be in `stored_codes/` directory

### Verify on Vercel:

1. Upload a file via your deployed website
2. Check your repository for the new commit
3. Verify the commit message: "Add {language} file: {title} via web upload"

## Additional Notes

- Commits are made with your GitHub token's associated account
- Each upload creates a separate commit
- Metadata updates are separate commits
- Large files (>16MB) are rejected before reaching GitHub
- GitHub API rate limits apply (5000 requests/hour for authenticated users)

## Support

If you encounter issues:
1. Check Vercel function logs
2. Verify token permissions on GitHub
3. Test with a simple file upload
4. Check the repository permissions

The application logs detailed information about GitHub operations for debugging.
