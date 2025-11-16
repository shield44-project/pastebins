#!/usr/bin/env python3
"""Test delete functionality"""

from app import app, load_code_metadata
import json

with app.test_client() as client:
    # Get initial count
    metadata_before = load_code_metadata('c')
    print(f'Initial C files: {len(metadata_before)}')
    
    # Try to delete the first file
    if len(metadata_before) > 0:
        first_file = metadata_before[0]
        print(f'\nAttempting to delete: {first_file["filename"]}')
        
        response = client.post('/delete/c/0', 
                              data=json.dumps({}),
                              content_type='application/json')
        
        print(f'Delete response status: {response.status_code}')
        
        if response.status_code == 200:
            result = json.loads(response.data)
            print(f'Delete result: {result}')
            
            # Check metadata after delete
            metadata_after = load_code_metadata('c')
            print(f'Files after delete: {len(metadata_after)}')
            
            if len(metadata_after) == len(metadata_before) - 1:
                print('✓ Delete successful - metadata updated')
            else:
                print('✗ Delete failed - metadata not updated correctly')
        else:
            print(f'✗ Delete failed with status {response.status_code}')
            print(response.data.decode('utf-8'))
    else:
        print('No files to delete')
