# Setup Encrypted Files Viewing

## Quick Setup

To view encrypted Python files in the repository, you need two things:

1. **Private Key File**: `private_key.pem`
2. **Token Secret**: "shield44" (already configured)

## Steps to Enable Encrypted File Viewing

### Option 1: Use Existing Private Key (Recommended)

If you have the original `private_key.pem` file that was used to encrypt the files:

1. Place your `private_key.pem` file in the root directory of the project:
   ```bash
   cp /path/to/your/private_key.pem ./private_key.pem
   ```

2. Make sure the file has the correct permissions:
   ```bash
   chmod 600 private_key.pem
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```

4. Navigate to `/encrypted-viewer` in your browser

5. Click on any encrypted file to view it (tokens are generated automatically)

### Option 2: Generate New Keys and Re-encrypt Files

If you don't have the original private key, you'll need to:

1. Generate a new keypair:
   ```bash
   python generate_keys.py --bits 4096
   ```
   This creates `private_key.pem` and updates `public_key.pem`

2. Re-encrypt your source files:
   ```bash
   # Place your unencrypted Python files in a source directory
   mkdir -p source
   cp your_files/*.py source/
   
   # Encrypt them
   python encrypt_files.py --public-key public_key.pem --source-dir ./source --delete-originals
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```

## Token Secret

The token secret is set to **"shield44"** by default. This is used to generate and validate access tokens for viewing encrypted files.

To change it, set the `TOKEN_SECRET` environment variable:
```bash
export TOKEN_SECRET=your_custom_secret
python app.py
```

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `private_key.pem` to version control (it's already in `.gitignore`)
- Keep `private_key.pem` secure and backed up
- The token secret "shield44" is for development/personal use
- For production deployment, use a strong, randomly generated secret

## Viewing Encrypted Files

Once setup is complete:

1. Start the Flask app: `python app.py`
2. Open browser to: `http://localhost:5000/encrypted-viewer`
3. Click any file to automatically decrypt and view it

The system automatically:
- Generates access tokens for each file
- Validates tokens server-side
- Decrypts files using the private key
- Displays decrypted content in a code editor

## Troubleshooting

### "Decryption not available (private key not found)"
- Make sure `private_key.pem` exists in the root directory
- Check file permissions: `ls -la private_key.pem`

### "Invalid or expired token"
- Tokens expire after 1 hour by default
- Refresh the page to get new tokens
- Check that TOKEN_SECRET matches what was used to generate tokens

### "Decryption failed"
- The private key doesn't match the public key used for encryption
- You may need to re-encrypt files with the current keypair

## API Endpoints

- `GET /encrypted-viewer` - Web interface for viewing encrypted files
- `GET /encrypted/list` - List all encrypted files with auto-generated tokens
- `GET /encrypted/file?name=<filename>&token=<token>` - Decrypt and retrieve file
- `GET /encrypted/token/<filename>` - Generate a token for a specific file

## More Information

See [ENCRYPTION_README.md](ENCRYPTION_README.md) for detailed documentation on the encryption system.
