#!/usr/bin/env python3
"""
Helper script to set up encryption for viewing encrypted files.

This script helps you set up the necessary private key for viewing
encrypted Python files in the repository.
"""

import os
import sys
from pathlib import Path

def main():
    print("=" * 70)
    print(" Encrypted Files Setup Helper")
    print("=" * 70)
    print()
    
    # Check if private_key.pem exists
    private_key_path = Path('private_key.pem')
    
    if private_key_path.exists():
        print("✓ private_key.pem found!")
        print()
        print("You can now view encrypted files:")
        print("  1. Run: python app.py")
        print("  2. Visit: http://localhost:5000/encrypted-viewer")
        print("  3. Click on any file to view it")
        print()
        return 0
    
    print("⚠ private_key.pem NOT FOUND")
    print()
    print("To view the encrypted files in this repository, you need the")
    print("private key that corresponds to the public_key.pem file.")
    print()
    print("=" * 70)
    print(" Choose an option:")
    print("=" * 70)
    print()
    print("Option 1: I have the original private_key.pem file")
    print("-" * 50)
    print("  Place your private_key.pem in the root directory:")
    print("    cp /path/to/your/private_key.pem ./private_key.pem")
    print("    chmod 600 private_key.pem")
    print()
    
    print("Option 2: I don't have the original key (for testing/development)")
    print("-" * 50)
    print("  Generate a NEW keypair (this will NOT work with existing encrypted files):")
    print("    python generate_keys.py --bits 4096")
    print()
    print("  Then re-encrypt your source files:")
    print("    mkdir -p source")
    print("    cp your_files/*.py source/")
    print("    python encrypt_files.py --public-key public_key.pem --source-dir ./source")
    print()
    
    print("=" * 70)
    print()
    print("The token secret is already configured to 'shield44'")
    print()
    print("For more information, see SETUP_ENCRYPTION.md")
    print()
    
    # Ask if user wants to generate new keys
    response = input("Generate new keypair now? (y/N): ").strip().lower()
    
    if response == 'y':
        print()
        print("Generating new RSA-4096 keypair...")
        import subprocess
        try:
            subprocess.run([sys.executable, 'generate_keys.py', '--bits', '4096'], check=True)
            print()
            print("⚠ NOTE: Existing encrypted files in ./encrypted/ will NOT be viewable")
            print("   with this new key. You'll need to re-encrypt them with your source files.")
            print()
        except subprocess.CalledProcessError:
            print("Error generating keys. Please run: python generate_keys.py")
            return 1
    else:
        print()
        print("No keys generated. Place your private_key.pem in the root directory to continue.")
        print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
