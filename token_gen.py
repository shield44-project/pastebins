#!/usr/bin/env python3
"""
Generate short-lived HMAC-signed tokens for file access.
Usage: python token_gen.py --filename example.py --ttl 3600 --secret mysecret
Generates URL-safe base64 token encoding filename:expiry:signature.
"""

import argparse
import base64
import hmac
import hashlib
import time
import os


def generate_token(filename, ttl, secret):
    """
    Generate HMAC-signed token for filename with TTL.
    Returns URL-safe base64 token: base64(filename:expiry:signature)
    """
    # Calculate expiry timestamp
    expiry = int(time.time()) + ttl
    
    # Create message: filename:expiry
    message = f"{filename}:{expiry}"
    
    # Generate HMAC signature
    signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Create full token: filename:expiry:signature
    token_data = f"{message}:{signature}"
    
    # Encode as URL-safe base64
    token = base64.urlsafe_b64encode(token_data.encode('utf-8')).decode('utf-8')
    
    return token


def main():
    parser = argparse.ArgumentParser(
        description='Generate HMAC-signed token for file access'
    )
    parser.add_argument(
        '--filename',
        required=True,
        help='Filename to generate token for'
    )
    parser.add_argument(
        '--ttl',
        type=int,
        default=3600,
        help='Time-to-live in seconds (default: 3600)'
    )
    parser.add_argument(
        '--secret',
        help='HMAC secret (or set TOKEN_SECRET env var)'
    )
    
    args = parser.parse_args()
    
    # Get secret from argument or environment
    secret = args.secret or os.environ.get('TOKEN_SECRET')
    if not secret:
        print("Error: Secret required via --secret or TOKEN_SECRET environment variable")
        return 1
    
    # Generate token
    token = generate_token(args.filename, args.ttl, secret)
    
    print(f"Token for '{args.filename}' (TTL: {args.ttl}s):")
    print(token)
    print(f"\nExample URL:")
    print(f"http://localhost:5000/file?name={args.filename}&token={token}")
    
    return 0


if __name__ == '__main__':
    exit(main())
