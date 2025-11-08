# Deployment Guide

This guide explains how to deploy the Code Storage Website in different environments.

## Table of Contents

1. [GitHub Pages Deployment (Static Pages Only)](#github-pages-deployment)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)

---

## GitHub Pages Deployment

### What Works on GitHub Pages

GitHub Pages only supports **static HTML/CSS/JavaScript files**. The following features work on GitHub Pages:

✅ **Landing Page** (`index.html`)
- Project overview and feature showcase
- Links to documentation
- Installation instructions

✅ **Encrypted File Viewer** (`viewer.html`)
- Standalone static page for viewing encrypted files
- Requires a separate decryption server (see `decrypt_server.py`)

### What Doesn't Work on GitHub Pages

❌ The following features require a Python backend and **cannot** run on GitHub Pages:
- Code execution (Python, Java, C, C++)
- Code upload and storage
- File management
- Dynamic content generation

### Automatic Deployment

This repository includes a GitHub Actions workflow that automatically deploys to GitHub Pages when changes are pushed to the `main` branch.

**File**: `.github/workflows/deploy.yml`

### Manual GitHub Pages Setup

1. Go to your repository settings on GitHub
2. Navigate to **Pages** section
3. Under **Source**, select:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
4. Click **Save**
5. Your site will be available at: `https://[username].github.io/[repository-name]/`

### Using the Encrypted File Viewer on GitHub Pages

To use the encrypted file viewer on GitHub Pages:

1. Deploy the decryption server separately (see [decrypt_server.py](decrypt_server.py))
2. Update the API endpoint in `viewer.html` if needed
3. Generate tokens using `token_gen.py`
4. Share tokens with authorized users

---

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Compilers for code execution:
  - Java JDK for Java support
  - GCC for C support
  - G++ for C++ support

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shield44-project/codes_storer_website.git
   cd codes_storer_website
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser**:
   ```
   http://localhost:5000
   ```

### Environment Variables

You can customize the application using environment variables:

```bash
# Flask configuration
export FLASK_DEBUG=True          # Enable debug mode (default: True)
export FLASK_HOST=0.0.0.0        # Host to bind (default: 0.0.0.0)
export FLASK_PORT=5000           # Port to use (default: 5000)

# Application configuration
export SECRET_KEY=your-secret-key-here  # Secret key for sessions
export CODES_DIRECTORY=stored_codes     # Directory for storing code files
```

### Development with Auto-reload

Flask's debug mode enables auto-reload when files change:

```bash
export FLASK_DEBUG=True
python app.py
```

---

## Production Deployment

### Security Considerations

⚠️ **Important**: Before deploying to production:

1. **Set a strong SECRET_KEY**:
   ```bash
   export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
   ```

2. **Disable debug mode**:
   ```bash
   export FLASK_DEBUG=False
   ```

3. **Use a production WSGI server** (not Flask's built-in server):
   - Gunicorn (recommended)
   - uWSGI
   - Waitress

### Deployment Options

#### Option 1: Using Gunicorn

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

#### Option 2: Using Docker

1. **Create a Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt gunicorn
   
   COPY . .
   
   ENV FLASK_DEBUG=False
   ENV SECRET_KEY=change-this-in-production
   
   EXPOSE 5000
   
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **Build and run**:
   ```bash
   docker build -t codes-storer .
   docker run -p 5000:5000 -e SECRET_KEY="your-secret" codes-storer
   ```

#### Option 3: Platform as a Service (PaaS)

**Heroku**:
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create
   git push heroku main
   ```

**Railway, Render, or Fly.io**:
- Follow their respective Python deployment guides
- Ensure environment variables are set
- Use Gunicorn as the production server

### Reverse Proxy Setup (Nginx)

For production, use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 30d;
    }
}
```

### SSL/TLS Certificate

Use Let's Encrypt for free SSL certificates:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Troubleshooting

### Code Execution Not Working

**Problem**: Code execution returns errors or doesn't work.

**Solutions**:
- Ensure the required compilers are installed
- Check that they are in your system PATH
- Verify file permissions in the temporary directory

### Port Already in Use

**Problem**: `Address already in use` error.

**Solutions**:
```bash
# Find the process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use a different port
export FLASK_PORT=5001
python app.py
```

### Permission Denied Errors

**Problem**: Cannot write to `stored_codes` directory.

**Solutions**:
```bash
# Set proper permissions
chmod 755 stored_codes
chown -R $USER:$USER stored_codes
```

### GitHub Pages Shows 404

**Problem**: GitHub Pages shows "404 - File not found".

**Solutions**:
1. Ensure `index.html` is in the root directory
2. Check GitHub Pages settings in repository settings
3. Wait a few minutes after pushing changes
4. Clear browser cache and try again

---

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/shield44-project/codes_storer_website/issues)
- Check the [README](README.md) for general documentation
- Review the [ENCRYPTION_README](ENCRYPTION_README.md) for encryption features

---

## License

This project is open source and available under the MIT License.
