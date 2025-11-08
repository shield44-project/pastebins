# Server-Side Encrypted File Viewer

This toolkit provides server-side encrypted file viewing with hybrid RSA+AES encryption and token-based authentication.

## Overview

The system enables storing encrypted Python source files in the repository and serving plaintext via a secure server-side decryption endpoint. It uses:

- **Hybrid RSA+AES Encryption**: Files are encrypted with AES-256-GCM, and the AES key is encrypted with RSA-4096-OAEP
- **Token-based Authentication**: Short-lived HMAC-SHA256 signed tokens control access to decrypted files
- **Server-side Decryption**: Files are decrypted on-demand on the server, never exposing private keys to clients

## Files

- `generate_keys.py` - RSA keypair generation tool
- `encrypt_files.py` - File encryption tool with hybrid scheme
- `token_gen.py` - Access token generation tool
- `decrypt_server.py` - Flask server for serving decrypted files
- `viewer.html` - Web-based viewer for encrypted files

## Quick Start

### 1. Generate RSA Keys

```bash
python generate_keys.py --bits 4096
```

This creates:
- `private_key.pem` - Keep this secure and OFF the repository!
- `public_key.pem` - Can be committed to the repository

⚠️ **IMPORTANT**: Never commit `private_key.pem` to version control!

### 2. Encrypt Files

```bash
# Create source directory with files to encrypt
mkdir -p source
cp my_script.py source/

# Encrypt files
python encrypt_files.py --public-key public_key.pem --source-dir ./source

# Optional: Delete originals after encryption
python encrypt_files.py --public-key public_key.pem --source-dir ./source --delete-originals
```

This creates:
- `encrypted/` directory with `.enc.json` files
- `encrypted/manifest.json` - Index of encrypted files

### 3. Start Decryption Server

```bash
python decrypt_server.py --port 5000 --secret mysecret --private-key private_key.pem
```

Or use environment variable for the secret:

```bash
export TOKEN_SECRET=mysecret
python decrypt_server.py --port 5000 --private-key private_key.pem
```

### 4. Generate Access Token

```bash
python token_gen.py --filename example.py --ttl 3600 --secret mysecret
```

This generates a token valid for 1 hour (3600 seconds).

### 5. View Encrypted Files

Open `viewer.html` in your browser at `http://localhost:5000/`

- Select a file from the list
- Paste the access token
- Click "Decrypt & View"

## Command Reference

### generate_keys.py

Generate RSA keypair for encryption:

```bash
python generate_keys.py [--bits BITS]
```

Options:
- `--bits` - Key size in bits (default: 4096)

### encrypt_files.py

Encrypt files with hybrid RSA+AES scheme:

```bash
python encrypt_files.py --public-key PUBLIC_KEY [options]
```

Options:
- `--public-key` - Path to RSA public key (required)
- `--source-dir` - Source directory to scan (default: ./source)
- `--patterns` - File patterns to match (default: *.py)
- `--delete-originals` - Delete original files after encryption

Examples:

```bash
# Encrypt all Python files
python encrypt_files.py --public-key public_key.pem --source-dir ./source

# Encrypt multiple file types
python encrypt_files.py --public-key public_key.pem --source-dir ./source --patterns "*.py" "*.txt"

# Encrypt and delete originals
python encrypt_files.py --public-key public_key.pem --source-dir ./source --delete-originals
```

### token_gen.py

Generate HMAC-signed access tokens:

```bash
python token_gen.py --filename FILENAME [options]
```

Options:
- `--filename` - Filename to generate token for (required)
- `--ttl` - Time-to-live in seconds (default: 3600)
- `--secret` - HMAC secret (or set TOKEN_SECRET env var)

Examples:

```bash
# Generate 1-hour token
python token_gen.py --filename example.py --ttl 3600 --secret mysecret

# Generate 10-minute token using environment variable
export TOKEN_SECRET=mysecret
python token_gen.py --filename example.py --ttl 600
```

### decrypt_server.py

Flask server for decrypting and serving files:

```bash
python decrypt_server.py [options]
```

Options:
- `--port` - Port to run server on (default: 5000)
- `--secret` - HMAC secret (or set TOKEN_SECRET env var)
- `--private-key` - Path to RSA private key (default: private_key.pem)
- `--encrypted-dir` - Directory with encrypted files (default: encrypted)

Endpoints:
- `GET /` - Serve viewer.html
- `GET /file?name=<filename>&token=<token>` - Decrypt and serve file
- `GET /manifest` - List encrypted files

Examples:

```bash
# Basic usage
python decrypt_server.py --secret mysecret

# Custom port and paths
python decrypt_server.py --port 8080 --secret mysecret --private-key keys/private.pem --encrypted-dir data/encrypted

# Using environment variable for secret
export TOKEN_SECRET=mysecret
python decrypt_server.py
```

## Security Notes

1. **Private Key Security**
   - Never commit `private_key.pem` to version control
   - Store it securely on the server
   - Use appropriate file permissions (chmod 600)

2. **Token Secret**
   - Use a strong, randomly generated secret
   - Never hard-code secrets in source code
   - Use environment variables in production

3. **HTTPS in Production**
   - Always use HTTPS in production
   - Use a production WSGI server (gunicorn, uWSGI)
   - Example: `gunicorn -w 4 -b 0.0.0.0:5000 decrypt_server:app`

4. **Token Expiry**
   - Use short TTL values (minutes, not days)
   - Regenerate tokens frequently
   - Consider implementing token revocation for sensitive data

5. **Encrypted Directory**
   - The `encrypted/` directory is gitignored by default
   - Repository owner should run encryption locally
   - Commit encrypted payloads separately if needed

## Architecture

```
┌─────────────┐
│   Source    │
│   Files     │
└──────┬──────┘
       │
       ├─ encrypt_files.py (uses public_key.pem)
       │
       ▼
┌─────────────┐
│  Encrypted  │
│   Files     │
│  (*.enc.json)│
└──────┬──────┘
       │
       │
       ├─ decrypt_server.py (uses private_key.pem)
       │  + token_gen.py (generates tokens)
       │
       ▼
┌─────────────┐
│   Client    │
│ (viewer.html)│
└─────────────┘
```

## Encryption Format

Each encrypted file is stored as JSON:

```json
{
  "orig_name": "example.py",
  "payload": {
    "encrypted_key": "<base64-encoded RSA-encrypted AES key>",
    "nonce": "<base64-encoded 96-bit nonce>",
    "ciphertext": "<base64-encoded AES-GCM ciphertext>"
  }
}
```

## Token Format

Tokens are URL-safe base64 encoded strings containing:

```
base64url(filename:expiry_timestamp:hmac_signature)
```

Where:
- `filename` - Original filename
- `expiry_timestamp` - Unix timestamp when token expires
- `hmac_signature` - HMAC-SHA256 signature of `filename:expiry_timestamp`

## Dependencies

```
Flask>=3.0.0
cryptography>=41.0.0
```

Install with:

```bash
pip install -r requirements.txt
```

## License

This project is open source and available under the MIT License.
