#!/usr/bin/env python3
"""
Generate RSA keypair for hybrid encryption scheme.
Usage: python generate_keys.py [--bits 4096]
Writes private_key.pem and public_key.pem. Keep private key OFF repository!
"""

import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def generate_keys(bits=4096):
    """Generate RSA keypair and save to PEM files."""
    print(f"Generating {bits}-bit RSA keypair...")
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend()
    )
    
    # Generate public key
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write to files
    with open('private_key.pem', 'wb') as f:
        f.write(private_pem)
    print("✓ Written private_key.pem")
    
    with open('public_key.pem', 'wb') as f:
        f.write(public_pem)
    print("✓ Written public_key.pem")
    
    print("\n⚠️  WARNING: Keep private_key.pem OFF the repository!")
    print("   Add private_key.pem to .gitignore")


def main():
    parser = argparse.ArgumentParser(
        description='Generate RSA keypair for file encryption'
    )
    parser.add_argument(
        '--bits',
        type=int,
        default=4096,
        help='RSA key size in bits (default: 4096)'
    )
    
    args = parser.parse_args()
    generate_keys(args.bits)


if __name__ == '__main__':
    main()
