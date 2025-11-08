#!/usr/bin/env python3
"""
Encrypt files with hybrid RSA+AES scheme.
Usage: python encrypt_files.py --public-key public_key.pem --source-dir ./source [--delete-originals]
Scans source directory for *.py files (or custom globs), encrypts with AES-GCM,
encrypts AES key with RSA public key, writes encrypted/<filename>.enc.json.
"""

import argparse
import os
import json
import glob
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


def load_public_key(public_key_path):
    """Load RSA public key from PEM file."""
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return public_key


def encrypt_file(file_path, public_key):
    """
    Encrypt a file using hybrid RSA+AES scheme.
    Returns dict with encrypted_key, nonce, and ciphertext (all base64).
    """
    # Read file content
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    # Generate random AES-256 key and 96-bit nonce
    aesgcm = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)  # 96 bits
    
    # Encrypt file with AES-GCM
    cipher = AESGCM(aesgcm)
    ciphertext = cipher.encrypt(nonce, plaintext, None)
    
    # Encrypt AES key with RSA public key (RSA-OAEP)
    encrypted_key = public_key.encrypt(
        aesgcm,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Return as base64-encoded strings for JSON serialization
    import base64
    return {
        'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
    }


def encrypt_files(source_dir, public_key_path, patterns, delete_originals=False):
    """Scan source directory and encrypt matching files."""
    # Load public key
    public_key = load_public_key(public_key_path)
    
    # Create encrypted directory
    encrypted_dir = Path('encrypted')
    encrypted_dir.mkdir(exist_ok=True)
    
    # Find files to encrypt
    files_to_encrypt = []
    for pattern in patterns:
        files_to_encrypt.extend(glob.glob(os.path.join(source_dir, pattern)))
    
    if not files_to_encrypt:
        print(f"No files found matching patterns {patterns} in {source_dir}")
        return
    
    manifest = {}
    
    for file_path in files_to_encrypt:
        orig_name = os.path.basename(file_path)
        print(f"Encrypting {orig_name}...")
        
        # Encrypt file
        payload = encrypt_file(file_path, public_key)
        
        # Create output filename
        enc_filename = f"{orig_name}.enc.json"
        enc_path = encrypted_dir / enc_filename
        
        # Write encrypted payload
        output = {
            'orig_name': orig_name,
            'payload': payload
        }
        with open(enc_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"  ✓ Written {enc_path}")
        
        # Add to manifest
        manifest[orig_name] = enc_filename
        
        # Delete original if requested
        if delete_originals:
            os.remove(file_path)
            print(f"  ✓ Deleted {file_path}")
    
    # Write manifest
    manifest_path = encrypted_dir / 'manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"\n✓ Written manifest: {manifest_path}")
    print(f"✓ Encrypted {len(files_to_encrypt)} file(s)")


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt files with hybrid RSA+AES encryption'
    )
    parser.add_argument(
        '--public-key',
        required=True,
        help='Path to RSA public key PEM file'
    )
    parser.add_argument(
        '--source-dir',
        default='./source',
        help='Source directory to scan (default: ./source)'
    )
    parser.add_argument(
        '--patterns',
        nargs='+',
        default=['*.py'],
        help='File patterns to match (default: *.py)'
    )
    parser.add_argument(
        '--delete-originals',
        action='store_true',
        help='Delete original files after encryption'
    )
    
    args = parser.parse_args()
    encrypt_files(
        args.source_dir,
        args.public_key,
        args.patterns,
        args.delete_originals
    )


if __name__ == '__main__':
    main()
