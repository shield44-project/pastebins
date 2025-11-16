# Code Storage Website

A comprehensive web application for storing, viewing, categorizing, and executing code files. This platform supports multiple programming languages and allows you to run HTML websites within the application.

**🎉 Now with TypeScript and React support!** The project includes a modern frontend built with TypeScript and React. See [TYPESCRIPT_REACT_SETUP.md](TYPESCRIPT_REACT_SETUP.md) for details.

## Features

### 📁 Code Storage & Organization
- Upload and store code files organized by language
- Support for Python, Java, C, C++, and HTML
- Add titles and descriptions to your code files
- Automatic categorization by programming language

### 👁️ Code Viewing
- Syntax-highlighted code editor (powered by CodeMirror)
- Beautiful, modern UI with dark theme editor
- View all your stored codes in organized categories

### ▶️ Code Execution
- Execute Python, Java, C, and C++ code directly in the browser
- Provide custom input (stdin) for interactive programs
- View program output and error messages in real-time
- Sandboxed execution with timeout limits for security

### 🌐 HTML Website Preview
- Upload complete HTML websites
- View HTML code with syntax highlighting
- **Live preview of HTML websites running inside the platform**
- Fullscreen mode for better viewing experience
- Copy code to clipboard
- Refresh preview on demand

### 🔐 Encrypted Code Storage
- **Server-side encrypted Python code examples**
- Hybrid RSA-4096 + AES-256-GCM encryption
- Token-based authentication with HMAC-SHA256
- View encrypted code files through secure web interface
- Code is decrypted server-side only (private key never exposed)
- Time-limited access tokens for enhanced security

### 📤 Multi-File Upload
- Upload single files or multiple files at once
- Support for folder/batch uploads
- Automatic file organization by language
- File preview before upload
- Drag-and-drop support (coming soon)

### ☁️ Vercel Blob Storage Integration
- **Persistent file storage for serverless deployments**
- Automatic file synchronization to Vercel Blob
- Files persist across deployments on Vercel
- Graceful fallback to local storage
- Works alongside GitHub integration
- See [VERCEL_BLOB_SETUP.md](VERCEL_BLOB_SETUP.md) for setup guide

### 📝 Notes with Screenshots
- **Create and store notes with rich text content**
- **Attach multiple screenshots/images to notes**
- Drag-and-drop image upload support
- Image gallery with thumbnail previews
- Edit and delete notes
- Stored locally in browser (localStorage) for static deployment
- Perfect for documentation, reminders, and visual references

## Supported Languages

| Language | Extension | Execution Support | Compilation |
|----------|-----------|-------------------|-------------|
| Python   | `.py`     | ✅ Yes            | No          |
| Java     | `.java`   | ✅ Yes            | Yes (javac) |
| C        | `.c`      | ✅ Yes            | Yes (gcc)   |
| C++      | `.cpp`    | ✅ Yes            | Yes (g++)   |
| HTML     | `.html`   | 🌐 Live Preview   | N/A         |

## GitHub Pages Deployment

### 🌐 Live Demo
Visit the live demo at: **https://shield44-project.github.io/codes_storer_website/**

The GitHub Pages deployment includes:
- A landing page explaining the project and features
- The encrypted file viewer (`viewer.html`) as a standalone static page

### ⚠️ Important Limitations
**This is primarily a Flask application that requires a Python backend server.** GitHub Pages only supports static HTML/CSS/JavaScript files and **cannot run the full application** with the following features:
- Code execution (Python, Java, C, C++)
- Code storage and upload
- File management

To use these features, you must run the application locally (see installation instructions below).

### What Works on GitHub Pages
- ✅ Project landing page with documentation
- ✅ Encrypted file viewer (requires separate decryption server)
- ✅ Static content and documentation

## Installation (Local Deployment)

### Prerequisites
- Python 3.8 or higher
- For code execution support, install:
  - Python 3 (for Python code execution)
  - Java JDK (for Java code execution)
  - GCC (for C code execution)
  - G++ (for C++ code execution)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/shield44-project/codes_storer_website.git
cd codes_storer_website
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

### Running with Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Configuration

The application can be configured using environment variables:

### Storage Configuration

**`CODES_DIRECTORY`** (optional)
- Directory for storing code files
- Default: `stored_codes`
- Example: `/tmp/stored_codes` (for serverless platforms)

**`shield44_READ_WRITE_TOKEN`** (optional, recommended for Vercel)
- Vercel Blob Storage read-write token for persistent storage
- Enables file persistence on serverless platforms
- See [VERCEL_BLOB_SETUP.md](VERCEL_BLOB_SETUP.md) for setup
- Example: `vercel_blob_rw_GmsSyO1ENI6nA5GJ_ETd7tIhY7RialiPNyz5YaP8U2EZTAZ`

### GitHub Integration (optional)

**`GITHUB_TOKEN`**
- GitHub Personal Access Token for automatic commits
- Requires `repo` scope
- See [GITHUB_INTEGRATION_SETUP.md](GITHUB_INTEGRATION_SETUP.md)

**`GITHUB_REPO`**
- Target repository for commits
- Default: `shield44-project/pastebins`

**`GITHUB_BRANCH`**
- Target branch for commits
- Default: `main`

### Flask Configuration

**`FLASK_DEBUG`**
- Enable debug mode (True/False)
- Default: False (production)

**`FLASK_HOST`**
- Server host
- Default: `0.0.0.0`

**`FLASK_PORT`**
- Server port
- Default: `5000`

## Usage Guide

### Uploading Code

**Single File Upload (Paste Code):**
1. Click on "Upload New Code" button on the home page
2. Select the "📝 Paste Code" tab
3. Select the language (Python, Java, C, C++, or HTML)
4. Enter a title for your code
5. Optionally add a description
6. Paste your code in the code editor
7. Click "Upload Code"

**Multiple File Upload:**
1. Click on "Upload New Code" button on the home page
2. Select the "📁 Upload Files" tab
3. Select the language
4. Click "Select Files" and choose one or more files
5. Preview the selected files
6. Click "Upload Files"

### Viewing Encrypted Python Code Examples

The repository includes encrypted Python code examples that can be viewed securely:

1. **Setup (First Time Only):**
   - Place your `private_key.pem` in the root directory OR
   - Run `python setup_encryption.py` for guided setup
   - See [SETUP_ENCRYPTION.md](SETUP_ENCRYPTION.md) for detailed instructions

2. **Viewing Files:**
   - Navigate to `/encrypted-viewer` on the running Flask app
   - Click on any Python file from the list
   - Files are automatically decrypted and displayed (no manual token entry needed!)

**Note:** The system uses "shield44" as the default token secret for generating access tokens. The private key (`private_key.pem`) must be present for decryption to work. See [SETUP_ENCRYPTION.md](SETUP_ENCRYPTION.md) for more details.

### Viewing and Executing Code

**For Programming Languages (Python, Java, C, C++):**
1. Navigate to a language category from the home page
2. Click on a code file to view it
3. Click "▶️ Run Code" to execute the code
4. Optionally provide input in the "Input (stdin)" field
5. View the output in the output panel

**For HTML Websites:**
1. Navigate to the HTML category
2. Click on an HTML file to view it
3. The left panel shows the HTML code
4. The right panel shows a **live preview of the website running**
5. Use the "🔄 Refresh" button to reload the preview
6. Use the "⛶ Fullscreen" button to view the website in fullscreen mode
7. Use the "📋 Copy Code" button to copy the HTML code

### Category Management

All uploaded files are automatically organized by language:
- Python files → Python category
- Java files → Java category
- C files → C category
- C++ files → C++ category
- HTML files → HTML category

## Project Structure

```
codes_storer_website/
├── app.py                  # Main Flask application (with encryption support)
├── config.py              # Configuration settings
├── encrypt_files.py       # Tool for encrypting Python files
├── decrypt_server.py      # Standalone decryption server
├── generate_keys.py       # RSA key generation tool
├── token_gen.py           # Access token generation tool
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── ENCRYPTION_README.md   # Encryption documentation
├── .gitignore            # Git ignore rules
├── public_key.pem        # RSA public key (committed)
├── private_key.pem       # RSA private key (NOT committed, server-only)
├── viewer.html           # Encrypted file viewer (standalone page)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── category.html     # Category listing page
│   ├── upload.html       # Upload form (with multi-file support)
│   ├── view_code.html    # Code viewer for executable languages
│   └── view_html.html    # HTML website viewer with live preview
├── static/               # Static assets
│   └── css/
│       └── style.css     # Stylesheet
├── encrypted/            # Encrypted Python code examples (committed)
│   ├── manifest.json     # Index of encrypted files
│   └── *.py.enc.json    # Encrypted Python files
└── stored_codes/         # Storage directory (auto-created, not committed)
    ├── python/           # Python files
    ├── java/             # Java files
    ├── c/                # C files
    ├── cpp/              # C++ files
    ├── html/             # HTML files
    └── *_metadata.json   # Metadata files
```

## Security Features

### Code Execution Security
- Code execution is sandboxed with 5-second timeout limits
- Temporary directory usage for compilation and execution
- Input sanitization for uploaded code
- HTML preview uses iframe with sandbox attributes
- No direct file system access from executed code
- Command injection prevention with shell=False

### Encrypted Code Storage
- **Hybrid RSA-4096 + AES-256-GCM encryption** for Python code examples
- **Server-side decryption only** - private key never exposed to clients
- **Token-based authentication** with HMAC-SHA256 signatures
- **Time-limited access tokens** (default 1 hour, configurable)
- Encrypted files stored in repository, safe to commit
- Private key must be kept secure on server (excluded from git)
- See [ENCRYPTION_README.md](ENCRYPTION_README.md) for detailed documentation

### File Upload Security
- File size limits (16MB max)
- File extension validation
- Filename sanitization to prevent path traversal
- Content-type validation

## Technologies Used

### Backend
- **Flask**: Python web framework
- **Python 3**: Core backend language
- **Cryptography**: RSA-OAEP, AES-GCM encryption
- **HMAC-SHA256**: Token-based authentication

### Frontend
- **TypeScript**: Type-safe JavaScript development
- **React**: Component-based UI framework
- **Webpack**: Module bundler and build tool
- **HTML5, CSS3**: Modern web standards
- **JavaScript (ES6+)**: Modern JavaScript features

### Development Tools
- **Node.js & npm**: Package management
- **ts-loader**: TypeScript compilation for Webpack
- **CodeMirror**: Syntax highlighting

### Code Execution
- **subprocess**: Python code execution
- **Compilers**: javac (Java), gcc (C), g++ (C++)

## Frontend Development

This project now includes a modern TypeScript/React frontend. For detailed information about the frontend setup, see [TYPESCRIPT_REACT_SETUP.md](TYPESCRIPT_REACT_SETUP.md).

### Quick Start (Frontend)

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

The React app runs on `http://localhost:3000` during development, while the Flask backend runs on `http://localhost:5000`.

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Code execution not working?
- Ensure the required compiler/interpreter is installed
- Check that the PATH environment variable includes the compiler/interpreter

### HTML preview not showing?
- Check browser console for errors
- Ensure the HTML file is valid
- Try the refresh button

### Upload failing?
- Check that the code syntax is valid
- Ensure title doesn't contain special characters
- Verify the file extension matches the selected language

## Future Enhancements

- Support for more languages (JavaScript, Ruby, Go, etc.)
- Collaborative code editing
- Code sharing via links
- Syntax checking before upload
- Code version history
- Search functionality
- Code comments and annotations

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

