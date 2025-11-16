"""
Vercel Blob Storage Integration Module

This module provides functions to interact with Vercel Blob storage
for storing and retrieving code files and metadata.
"""

import os
import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime


class VercelBlobStorage:
    """
    Vercel Blob Storage client for Python Flask applications.
    Uses the Vercel Blob HTTP API for file operations.
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize Vercel Blob Storage client.
        
        Args:
            token: Vercel Blob read-write token. If None, reads from environment variable.
        """
        self.token = token or os.environ.get('shield44_READ_WRITE_TOKEN')
        if not self.token:
            raise ValueError("shield44_READ_WRITE_TOKEN not provided and not found in environment")
        
        # Remove any 'vercel_blob_rw_' prefix if present (normalized token format)
        if self.token.startswith('vercel_blob_rw_'):
            self.token = self.token
        
        self.base_url = 'https://blob.vercel-storage.com'
        self.enabled = bool(self.token)
    
    def put(self, pathname: str, content: str, content_type: str = 'text/plain') -> Dict[str, Any]:
        """
        Upload a file to Vercel Blob storage.
        
        Args:
            pathname: The path where the file will be stored (e.g., 'stored_codes/python/hello.py')
            content: The file content as string
            content_type: MIME type of the content
        
        Returns:
            Dict with 'url', 'downloadUrl', 'pathname', 'contentType', 'contentDisposition'
        
        Raises:
            Exception: If upload fails
        """
        if not self.enabled:
            raise Exception("Blob storage not enabled - token not configured")
        
        try:
            # Vercel Blob API endpoint
            url = f"{self.base_url}/put"
            
            # Query parameters
            params = {
                'pathname': pathname,
                'access': 'public',  # Make files publicly accessible
            }
            
            # Headers
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': content_type,
            }
            
            # Upload the file
            response = requests.put(
                url,
                params=params,
                headers=headers,
                data=content.encode('utf-8') if isinstance(content, str) else content,
                timeout=30
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to upload to blob storage: {response.status_code} - {response.text}")
            
            result = response.json()
            return result
            
        except requests.RequestException as e:
            raise Exception(f"Network error uploading to blob storage: {str(e)}")
        except Exception as e:
            raise Exception(f"Error uploading to blob storage: {str(e)}")
    
    def get(self, url: str) -> str:
        """
        Download a file from Vercel Blob storage.
        
        Args:
            url: The blob URL (downloadUrl from put operation)
        
        Returns:
            File content as string
        
        Raises:
            Exception: If download fails
        """
        if not self.enabled:
            raise Exception("Blob storage not enabled - token not configured")
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"Failed to download from blob storage: {response.status_code}")
            
            return response.text
            
        except requests.RequestException as e:
            raise Exception(f"Network error downloading from blob storage: {str(e)}")
        except Exception as e:
            raise Exception(f"Error downloading from blob storage: {str(e)}")
    
    def delete(self, url: str) -> bool:
        """
        Delete a file from Vercel Blob storage.
        
        Args:
            url: The blob URL to delete
        
        Returns:
            True if successful
        
        Raises:
            Exception: If deletion fails
        """
        if not self.enabled:
            raise Exception("Blob storage not enabled - token not configured")
        
        try:
            # Vercel Blob API delete endpoint
            delete_url = f"{self.base_url}/delete"
            
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
            }
            
            payload = {
                'urls': [url]  # Can delete multiple URLs at once
            }
            
            response = requests.post(
                delete_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code not in [200, 204]:
                raise Exception(f"Failed to delete from blob storage: {response.status_code} - {response.text}")
            
            return True
            
        except requests.RequestException as e:
            raise Exception(f"Network error deleting from blob storage: {str(e)}")
        except Exception as e:
            raise Exception(f"Error deleting from blob storage: {str(e)}")
    
    def list_blobs(self, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List blobs with an optional prefix filter.
        
        Args:
            prefix: Optional prefix to filter blobs (e.g., 'stored_codes/python/')
        
        Returns:
            List of blob metadata dictionaries
        
        Raises:
            Exception: If listing fails
        """
        if not self.enabled:
            raise Exception("Blob storage not enabled - token not configured")
        
        try:
            list_url = f"{self.base_url}/list"
            
            headers = {
                'Authorization': f'Bearer {self.token}',
            }
            
            params = {}
            if prefix:
                params['prefix'] = prefix
            
            response = requests.get(
                list_url,
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to list blobs: {response.status_code} - {response.text}")
            
            result = response.json()
            return result.get('blobs', [])
            
        except requests.RequestException as e:
            raise Exception(f"Network error listing blobs: {str(e)}")
        except Exception as e:
            raise Exception(f"Error listing blobs: {str(e)}")


def get_blob_client() -> Optional[VercelBlobStorage]:
    """
    Get a Vercel Blob Storage client instance if configured.
    
    Returns:
        VercelBlobStorage instance if token is configured, None otherwise
    """
    try:
        token = os.environ.get('shield44_READ_WRITE_TOKEN')
        if token:
            return VercelBlobStorage(token)
        return None
    except Exception:
        return None


def is_blob_storage_enabled() -> bool:
    """
    Check if Vercel Blob storage is configured and enabled.
    
    Returns:
        True if blob storage is enabled, False otherwise
    """
    return bool(os.environ.get('shield44_READ_WRITE_TOKEN'))
