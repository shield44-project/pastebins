# Code Storage Website

A comprehensive web application for storing, viewing, categorizing, and executing code files. This platform supports multiple programming languages and allows you to run HTML websites within the application.

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

## Supported Languages

| Language | Extension | Execution Support | Compilation |
|----------|-----------|-------------------|-------------|
| Python   | `.py`     | ✅ Yes            | No          |
| Java     | `.java`   | ✅ Yes            | Yes (javac) |
| C        | `.c`      | ✅ Yes            | Yes (gcc)   |
| C++      | `.cpp`    | ✅ Yes            | Yes (g++)   |
| HTML     | `.html`   | 🌐 Live Preview   | N/A         |

## Installation

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

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Uploading Code

1. Click on "Upload New Code" button on the home page
2. Select the language (Python, Java, C, C++, or HTML)
3. Enter a title for your code
4. Optionally add a description
5. Paste your code in the code editor
6. Click "Upload Code"

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
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── category.html     # Category listing page
│   ├── upload.html       # Upload form
│   ├── view_code.html    # Code viewer for executable languages
│   └── view_html.html    # HTML website viewer with live preview
├── static/               # Static assets
│   └── css/
│       └── style.css     # Stylesheet
└── stored_codes/         # Storage directory (auto-created)
    ├── python/           # Python files
    ├── java/             # Java files
    ├── c/                # C files
    ├── cpp/              # C++ files
    ├── html/             # HTML files
    └── *_metadata.json   # Metadata files
```

## Security Features

- Code execution is sandboxed with 5-second timeout limits
- Temporary directory usage for compilation and execution
- Input sanitization for uploaded code
- HTML preview uses iframe with sandbox attributes
- No direct file system access from executed code

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Code Editor**: CodeMirror (syntax highlighting)
- **Styling**: Custom CSS with responsive design
- **Code Execution**: subprocess (Python), compilers (javac, gcc, g++)

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

