# Implementation Changes - Password-Based Encryption and Secret Folders

## Overview
This document describes the changes made to implement password-based encryption for file uploads and secret folder functionality, replacing the old RSA-based encryption system.

## Changes Made

### 1. Removed Old RSA-Based Encryption System

**Files Modified:**
- `app.py`: Removed RSA encryption functions, PRIVATE_KEY loading, token generation/verification, and encrypted file viewer routes
- `templates/base.html`: Updated navigation to replace "Encrypted Files" with "Secret Folders"
- `templates/index.html`: Updated action buttons to include Secret Folders link

**Functionality Removed:**
- RSA-4096 + AES-GCM hybrid encryption
- Token-based file access with HMAC signatures
- `/encrypted-viewer`, `/encrypted/manifest`, `/encrypted/file`, `/encrypted/token/*`, `/encrypted/list` routes
- Private key dependency

**Note:** The old `encrypted/` directory with RSA-encrypted files still exists but is no longer used. All Python sample files already exist in normal format in `stored_codes/python/`.

### 2. Implemented Password-Based Encryption

**Files Modified:**
- `app.py`: Added new encryption/decryption functions using password-based cryptography
- `templates/upload.html`: Added encryption toggle and password fields for both paste and file upload

**New Functions:**
```python
derive_key_from_password(password: str, salt: bytes) -> bytes
encrypt_content_with_password(content: str, password: str) -> dict
decrypt_content_with_password(encrypted_data: dict, password: str) -> str
```

**Encryption Scheme:**
- **Algorithm**: AES-256-GCM
- **Key Derivation**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000
- **Salt**: Random 128 bits per file
- **Nonce**: Random 96 bits per file
- **Storage Format**: JSON file with `.enc` extension containing salt, nonce, and ciphertext (all base64 encoded)

**Upload Flow:**
1. User checks "Encrypt this file with password" checkbox
2. Password field becomes visible and required
3. On submit, content is encrypted with provided password
4. Encrypted data stored as `filename.ext.enc` (JSON format)
5. Metadata marked with `"encrypted": true`

### 3. Implemented Decryption Functionality

**Files Modified:**
- `app.py`: Added `/decrypt/<language>/<code_id>` endpoint
- `templates/view_code.html`: Added password prompt UI and decryption handler

**New Route:**
```python
@app.route('/decrypt/<language>/<int:code_id>', methods=['POST'])
def decrypt_code(language, code_id):
```

**Viewing Encrypted Files:**
1. When viewing encrypted file, password prompt is displayed instead of code
2. User enters password and clicks "Decrypt"
3. AJAX request sent to `/decrypt` endpoint
4. On success: Code editor initialized with decrypted content
5. On failure: Error message displayed (wrong password or corrupted file)

### 4. Added Secret Folders Feature

**Files Created:**
- `templates/secret_folders.html`: New template for viewing all secret files

**Files Modified:**
- `app.py`: Added `is_secret` flag handling, filtered views, new routes
- `templates/upload.html`: Added "Mark as secret" checkbox
- `templates/category.html`: Added secret/public toggle button and badges
- `templates/index.html`: Added Secret Folders button

**New Routes:**
```python
@app.route('/secret-folders')
def secret_folders():
```

**Functionality:**
- Upload form includes "Mark as secret" checkbox
- Metadata includes `"is_secret": true/false` flag
- Category views filter out secret files by default
- `?show_secret=true` parameter shows only secret files
- `/secret-folders` page shows all secret files across all languages
- Visual badges (🔒 for encrypted, 🔐 for secret)

### 5. Updated File Metadata Schema

**New Fields:**
```json
{
  "title": "File Title",
  "description": "Description",
  "filename": "file.py",
  "created_at": "2025-11-09T16:53:21.231042",
  "encrypted": true,     // NEW: indicates if file is encrypted
  "is_secret": false     // NEW: indicates if file is secret
}
```

## Security Considerations

### Password-Based Encryption Security
- **Strong Key Derivation**: PBKDF2 with 100,000 iterations makes brute-force attacks computationally expensive
- **Unique Salts**: Each file gets a random salt, preventing rainbow table attacks
- **Unique Nonces**: Each file gets a random nonce for AES-GCM
- **Authenticated Encryption**: AES-GCM provides both confidentiality and authenticity

### Path Injection Mitigation
All file operations validated through:
1. Language parameter validated against LANGUAGES whitelist
2. Filename sanitization removes path separators
3. Filenames from controlled metadata, not direct user input
4. Path operations use `os.path.join()` safely

### Input Validation
- Title sanitized: removes path separators, special characters
- Language: validated against LANGUAGES dict
- Password: required when encryption enabled
- File extensions: validated against expected language extension

## Testing Performed

### Manual Testing Results
✅ **Upload normal file**: Creates `.py` file with correct content  
✅ **Upload encrypted file**: Creates `.py.enc` with encrypted JSON  
✅ **Upload secret file**: File hidden from normal category view  
✅ **Decrypt with correct password**: Returns plaintext successfully  
✅ **Decrypt with wrong password**: Returns error message  
✅ **View secret files**: Shows in secret folders page  
✅ **Filter secret files**: Not visible in normal category  
✅ **Navigation**: All links work correctly  

### Example Encrypted File Structure
```json
{
    "salt": "l/RYhE6ljp2pG7M40xkYKg==",
    "nonce": "TMiooV5GLtONWklZ",
    "ciphertext": "StAONTNLpTs0DkeHcpmI1Btdy4xlU6UG85BNJxxWw00VW9gV"
}
```

## User Guide

### Uploading Encrypted Files
1. Go to Upload page
2. Fill in language, title, and code
3. Check "🔒 Encrypt this file with password"
4. Enter a strong password (remember it!)
5. Click "Upload Code"

### Viewing Encrypted Files
1. Navigate to the encrypted file
2. Enter password in the prompt
3. Click "Decrypt"
4. Code will be displayed if password is correct

### Using Secret Folders
1. When uploading, check "🔐 Mark as secret"
2. Secret files won't appear in normal category listings
3. Click "🔐 Secret Folders" in navigation to view all secret files
4. Or use "View Secret Files" button in category pages

## Migration Notes

### For Existing Installations
- Old RSA-encrypted files in `encrypted/` directory are no longer used
- All Python sample files already exist in normal format
- No data migration required
- Old encrypted files can be kept for archival purposes or deleted

### Breaking Changes
- `/encrypted-viewer` and related routes removed
- RSA encryption system completely removed
- No backward compatibility with old encrypted files

## Dependencies
No new dependencies added. Uses existing cryptography library for:
- `AESGCM` (already used in old system)
- `PBKDF2HMAC` (standard in cryptography library)
- `hashes` (already used in old system)

## Future Enhancements
Potential improvements for future versions:
- Password strength meter
- Password recovery mechanism (e.g., security questions)
- Shared secret folders with password
- File-level permissions
- Encryption for other file types (not just code)
