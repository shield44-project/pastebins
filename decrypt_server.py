#!/usr/bin/env python3
"""
Flask server for decrypting files with token-based authentication.
Usage: python decrypt_server.py [--port 5000] [--secret mysecret] [--private-key private_key.pem]
Exposes /file?name=<filename>&token=<token> endpoint for decryption.
"""

import argparse
import os
import json
import base64
import hmac
import hashlib
import time
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


app = Flask(__name__)

# Global configuration (set via CLI or environment)
CONFIG = {
    'secret': None,
    'private_key': None,
    'encrypted_dir': 'encrypted'
}


def verify_token(token, filename, secret):
    """
    Verify HMAC token and check expiry.
    Returns True if valid, False otherwise.
    """
    try:
        # Decode from URL-safe base64
        token_data = base64.urlsafe_b64decode(token).decode('utf-8')
        
        # Parse: filename:expiry:signature
        parts = token_data.rsplit(':', 1)
        if len(parts) != 2:
            return False
        
        message, signature = parts
        
        # Check filename and expiry
        msg_parts = message.split(':', 1)
        if len(msg_parts) != 2:
            return False
        
        token_filename, expiry_str = msg_parts
        
        # Verify filename matches
        if token_filename != filename:
            return False
        
        # Check expiry
        expiry = int(expiry_str)
        if time.time() > expiry:
            return False
        
        # Verify HMAC signature
        expected_sig = hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_sig)
    
    except Exception as e:
        print(f"Token verification error: {e}")
        return False


def load_private_key(private_key_path):
    """Load RSA private key from PEM file."""
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    return private_key


def decrypt_file(encrypted_data, private_key):
    """
    Decrypt file using hybrid RSA+AES scheme.
    encrypted_data should have: encrypted_key, nonce, ciphertext (all base64).
    Returns plaintext bytes.
    """
    # Decode from base64
    encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
    nonce = base64.b64decode(encrypted_data['nonce'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    
    # Decrypt AES key with RSA private key
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Decrypt file content with AES-GCM
    cipher = AESGCM(aes_key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    
    return plaintext


@app.route('/file')
def serve_file():
    """
    Serve decrypted file if valid token provided.
    Query params: name=<filename>, token=<token>
    """
    filename = request.args.get('name')
    token = request.args.get('token')
    
    if not filename or not token:
        return jsonify({'error': 'Missing name or token parameter'}), 400
    
    # Verify token
    if not verify_token(token, filename, CONFIG['secret']):
        return jsonify({'error': 'Invalid or expired token'}), 403
    
    # Load encrypted file
    enc_filename = f"{filename}.enc.json"
    enc_path = Path(CONFIG['encrypted_dir']) / enc_filename
    
    if not enc_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    try:
        with open(enc_path, 'r') as f:
            encrypted_data = json.load(f)
        
        # Decrypt file
        plaintext = decrypt_file(
            encrypted_data['payload'],
            CONFIG['private_key']
        )
        
        # Return plaintext
        return plaintext, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    except Exception as e:
        print(f"Decryption error: {e}")
        return jsonify({'error': 'Decryption failed'}), 500


@app.route('/')
def index():
    """Serve viewer page."""
    return send_from_directory('.', 'viewer.html')


@app.route('/manifest')
def manifest():
    """Serve encrypted files manifest."""
    manifest_path = Path(CONFIG['encrypted_dir']) / 'manifest.json'
    if not manifest_path.exists():
        return jsonify({'error': 'Manifest not found'}), 404
    
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    return jsonify(data)


def main():
    parser = argparse.ArgumentParser(
        description='Flask server for encrypted file decryption'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run server on (default: 5000)'
    )
    parser.add_argument(
        '--secret',
        help='HMAC secret (or set TOKEN_SECRET env var)'
    )
    parser.add_argument(
        '--private-key',
        default='private_key.pem',
        help='Path to RSA private key (default: private_key.pem)'
    )
    parser.add_argument(
        '--encrypted-dir',
        default='encrypted',
        help='Directory with encrypted files (default: encrypted)'
    )
    
    args = parser.parse_args()
    
    # Get secret from argument or environment
    secret = args.secret or os.environ.get('TOKEN_SECRET')
    if not secret:
        print("Error: Secret required via --secret or TOKEN_SECRET environment variable")
        return 1
    
    # Load private key
    try:
        private_key = load_private_key(args.private_key)
    except Exception as e:
        print(f"Error loading private key: {e}")
        return 1
    
    # Set global config
    CONFIG['secret'] = secret
    CONFIG['private_key'] = private_key
    CONFIG['encrypted_dir'] = args.encrypted_dir
    
    print(f"Starting decryption server on port {args.port}...")
    print(f"Using private key: {args.private_key}")
    print(f"Encrypted files directory: {args.encrypted_dir}")
    
    app.run(host='0.0.0.0', port=args.port, debug=False)
    
    return 0


if __name__ == '__main__':
    exit(main())
