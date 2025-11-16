#!/usr/bin/env python3
"""Test if codes are being displayed"""

from app import app, load_code_metadata

with app.test_client() as client:
    # Test C category
    response = client.get('/category/c')
    print('Status:', response.status_code)
    print('Content length:', len(response.data))
    
    # Check metadata
    metadata = load_code_metadata('c')
    print('C metadata entries:', len(metadata))
    
    # Check response content
    content = response.data.decode('utf-8')
    if 'code-item' in content:
        print('✓ Found code-item in response')
        count = content.count('code-item')
        print(f'  Number of code items: {count}')
    else:
        print('✗ No code-item found in response')
        if 'No' in content and 'code files yet' in content:
            print('  Shows "No code files yet" message')
        
        # Look for what's actually in the codes list
        if '{% if codes %}' in content:
            print('  Template not rendered correctly')
        
        # Check if empty state is shown
        if 'empty-state' in content:
            print('  ✗ Empty state is being shown even though we have files!')
