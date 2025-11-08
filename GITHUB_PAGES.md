# GitHub Pages Setup Guide

This guide explains how to enable GitHub Pages for this repository using the `/root` location.

## Quick Setup (Recommended)

After merging this PR to the main branch:

1. **Go to Repository Settings**
   - Navigate to your repository on GitHub
   - Click on "Settings" tab

2. **Navigate to Pages**
   - In the left sidebar, click on "Pages"

3. **Configure Source**
   - Under "Build and deployment"
   - **Source**: Select "GitHub Actions"
   - That's it! The workflow is already configured

4. **Wait for Deployment**
   - Go to "Actions" tab
   - Watch the "Deploy to GitHub Pages" workflow run
   - Once complete, your site will be live

5. **Access Your Site**
   - URL: `https://[your-username].github.io/codes_storer_website/`
   - Or click the link shown in Pages settings

## Alternative Setup (Branch Deployment)

If you prefer to deploy from a branch instead of GitHub Actions:

1. **Go to Pages Settings** (same as above)

2. **Configure Source**
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main`
   - **Folder**: Select `/ (root)`
   - Click "Save"

3. **Wait for Deployment**
   - GitHub will automatically deploy
   - Check "Actions" tab for progress

## What Gets Deployed

When deployed to GitHub Pages, the following files are served:

- ✅ `index.html` - Landing page (entry point)
- ✅ `viewer.html` - Encrypted file viewer
- ✅ `static/` - CSS and other static assets
- ✅ `README.md`, `DEPLOYMENT.md` - Documentation (via links)

**Note**: Python files (.py) are included in the repository but won't execute on GitHub Pages.

## Verifying Deployment

1. **Check Deployment Status**
   - Go to "Actions" tab
   - Look for "pages build and deployment" workflow
   - Green checkmark = successful deployment

2. **View Your Site**
   - Click on the deployment
   - Find the URL in the workflow summary
   - Visit the URL to see your landing page

3. **Test Features**
   - Landing page should load with purple gradient background
   - Click "🔐 Open Encrypted File Viewer" to test viewer.html
   - All links should work

## Troubleshooting

### Issue: 404 Error on GitHub Pages

**Solution**:
- Ensure `index.html` exists in the root directory ✅
- Check Pages settings are configured correctly
- Wait 1-2 minutes for DNS propagation
- Clear browser cache and try again

### Issue: Workflow Not Running

**Solution**:
- Ensure `.github/workflows/deploy.yml` exists ✅
- Check that Pages source is set to "GitHub Actions"
- Verify workflow has proper permissions in Settings > Actions

### Issue: Some Files Not Loading

**Solution**:
- Check file paths are relative (no absolute paths)
- Ensure files are committed to the main branch
- Verify .gitignore doesn't exclude needed files

### Issue: Viewer.html Shows "No Files"

**Expected Behavior**: 
- This is normal! The viewer requires a separate decryption server
- The viewer.html works correctly, but needs encrypted files and a running decrypt_server.py
- See ENCRYPTION_README.md for details

## Understanding Limitations

### ✅ What Works on GitHub Pages:
- Static HTML pages (index.html, viewer.html)
- CSS styling
- JavaScript functionality
- Client-side features

### ❌ What Doesn't Work on GitHub Pages:
- Flask backend (app.py)
- Code execution features
- File upload/storage
- Server-side processing
- Database operations

**For full functionality**, deploy the Flask application locally or on a server. See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions.

## Custom Domain (Optional)

To use a custom domain:

1. **Add CNAME file** to repository root:
   ```
   your-domain.com
   ```

2. **Configure DNS** with your domain provider:
   ```
   Type: CNAME
   Name: www (or @)
   Value: [username].github.io
   ```

3. **Update Pages Settings**:
   - Enter your custom domain
   - Enable "Enforce HTTPS"

## Updating Your Site

After making changes:

1. **Commit and push** to main branch:
   ```bash
   git add .
   git commit -m "Update site content"
   git push origin main
   ```

2. **Wait for deployment**:
   - GitHub Actions will automatically deploy
   - Check "Actions" tab for progress
   - Usually takes 1-2 minutes

3. **Verify changes**:
   - Visit your GitHub Pages URL
   - Refresh the page (Ctrl+F5 for hard refresh)

## Security Considerations

✅ **Safe to Deploy**:
- No secrets or API keys in static files
- No sensitive data exposed
- Client-side code only

⚠️ **Not Deployed**:
- Python files are in repo but don't execute
- No server-side code runs
- Backend features require separate deployment

## Support

- 📖 See [README.md](README.md) for general documentation
- 🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for server deployment
- 🔐 See [ENCRYPTION_README.md](ENCRYPTION_README.md) for encryption features
- 🐛 [Open an issue](https://github.com/shield44-project/codes_storer_website/issues) for problems

## Success Checklist

After setup, verify:

- [ ] GitHub Pages is enabled in settings
- [ ] Workflow runs successfully in Actions tab
- [ ] Landing page loads at GitHub Pages URL
- [ ] Viewer.html is accessible
- [ ] All links work correctly
- [ ] No 404 errors
- [ ] Mobile responsive design works

**Congratulations! Your site is now live on GitHub Pages! 🎉**

---

**Need the full application?** Follow the local deployment guide in [DEPLOYMENT.md](DEPLOYMENT.md).
