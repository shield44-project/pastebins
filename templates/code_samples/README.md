# Code Samples (Reference)

This directory contains the original code samples that were used to populate the application's storage system. These are reference copies and are not directly used by the application during runtime.

## Directory Structure

```
code_samples/
├── python/     - Python code examples (.py)
├── c/          - C programming examples (.c)
├── cpp/        - C++ programming examples (.cpp)
└── html/       - HTML/CSS examples (.html)
```

## Languages Covered

### Python
- Basic algorithms
- Data structures
- File handling
- Mathematical computations
- Game logic
- Cryptography examples

### C
- Pointers and memory management
- Arrays and strings
- Functions
- Structures
- File I/O
- Control flow examples

### C++
- Templates
- Object-oriented programming
- Advanced data structures
- Modern C++ features

### HTML
- CSS Grid layouts
- Flexbox examples
- 3D CSS transformations
- Responsive design patterns

## Important Note

**The actual code files used by the application are stored in the `stored_codes/` directory at the root level.**

The migration script (`migrate_code_files.py`) copied files from this location to `stored_codes/` when setting up the application. These files in `code_samples/` are kept for:

1. **Reference and backup**
2. **Future migrations or updates**
3. **Documentation of original code samples**

## Adding New Code

If you want to add new code to the application, you should:
1. Use the web interface's upload feature, OR
2. Add files directly to the `stored_codes/` directory with appropriate metadata files

Do not add files here expecting them to appear in the application - they won't be loaded automatically.
