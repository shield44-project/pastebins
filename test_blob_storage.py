"""
Test Vercel Blob Storage Integration

This test module validates the Vercel Blob Storage integration.
"""

import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blob_storage import VercelBlobStorage, get_blob_client, is_blob_storage_enabled


class TestVercelBlobStorage(unittest.TestCase):
    """Test cases for Vercel Blob Storage integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_token = 'vercel_blob_rw_test_token_12345'
        self.test_content = 'print("Hello, World!")'
        self.test_pathname = 'test/hello.py'
        
    @patch.dict(os.environ, {'BLOB_READ_WRITE_TOKEN': ''}, clear=False)
    def test_blob_storage_disabled_when_no_token(self):
        """Test that blob storage is disabled when token is not configured"""
        self.assertFalse(is_blob_storage_enabled())
        client = get_blob_client()
        self.assertIsNone(client)
    
    @patch.dict(os.environ, {'BLOB_READ_WRITE_TOKEN': 'vercel_blob_rw_test'}, clear=False)
    def test_blob_storage_enabled_when_token_set(self):
        """Test that blob storage is enabled when token is configured"""
        self.assertTrue(is_blob_storage_enabled())
        client = get_blob_client()
        self.assertIsNotNone(client)
        self.assertIsInstance(client, VercelBlobStorage)
    
    def test_blob_client_initialization(self):
        """Test VercelBlobStorage client initialization"""
        client = VercelBlobStorage(self.test_token)
        self.assertEqual(client.token, self.test_token)
        self.assertTrue(client.enabled)
        self.assertEqual(client.base_url, 'https://blob.vercel-storage.com')
    
    def test_blob_client_requires_token(self):
        """Test that VercelBlobStorage raises error without token"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                VercelBlobStorage()
    
    @patch('blob_storage.requests.put')
    def test_put_file_success(self, mock_put):
        """Test successful file upload to blob storage"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'url': 'https://blob.vercel-storage.com/test.py',
            'downloadUrl': 'https://blob.vercel-storage.com/test.py',
            'pathname': self.test_pathname,
            'contentType': 'text/x-python'
        }
        mock_put.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        result = client.put(self.test_pathname, self.test_content, 'text/x-python')
        
        self.assertIn('url', result)
        self.assertIn('downloadUrl', result)
        self.assertEqual(result['pathname'], self.test_pathname)
        
        # Verify request was made correctly
        mock_put.assert_called_once()
        call_args = mock_put.call_args
        self.assertIn('Bearer', call_args[1]['headers']['Authorization'])
    
    @patch('blob_storage.requests.put')
    def test_put_file_failure(self, mock_put):
        """Test handling of failed file upload"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_put.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        
        with self.assertRaises(Exception) as context:
            client.put(self.test_pathname, self.test_content)
        
        self.assertIn('Failed to upload', str(context.exception))
    
    @patch('blob_storage.requests.get')
    def test_get_file_success(self, mock_get):
        """Test successful file download from blob storage"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.test_content
        mock_get.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        test_url = 'https://blob.vercel-storage.com/test.py'
        content = client.get(test_url)
        
        self.assertEqual(content, self.test_content)
        mock_get.assert_called_once_with(test_url, timeout=30)
    
    @patch('blob_storage.requests.get')
    def test_get_file_failure(self, mock_get):
        """Test handling of failed file download"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        test_url = 'https://blob.vercel-storage.com/nonexistent.py'
        
        with self.assertRaises(Exception) as context:
            client.get(test_url)
        
        self.assertIn('Failed to download', str(context.exception))
    
    @patch('blob_storage.requests.post')
    def test_delete_file_success(self, mock_post):
        """Test successful file deletion from blob storage"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        test_url = 'https://blob.vercel-storage.com/test.py'
        result = client.delete(test_url)
        
        self.assertTrue(result)
        
        # Verify delete request
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn('Bearer', call_args[1]['headers']['Authorization'])
        self.assertEqual(call_args[1]['json']['urls'], [test_url])
    
    @patch('blob_storage.requests.post')
    def test_delete_file_failure(self, mock_post):
        """Test handling of failed file deletion"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_post.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        test_url = 'https://blob.vercel-storage.com/test.py'
        
        with self.assertRaises(Exception) as context:
            client.delete(test_url)
        
        self.assertIn('Failed to delete', str(context.exception))
    
    @patch('blob_storage.requests.get')
    def test_list_blobs_success(self, mock_get):
        """Test successful listing of blobs"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'blobs': [
                {'url': 'https://blob.vercel-storage.com/file1.py', 'pathname': 'stored_codes/python/file1.py'},
                {'url': 'https://blob.vercel-storage.com/file2.py', 'pathname': 'stored_codes/python/file2.py'}
            ]
        }
        mock_get.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        blobs = client.list_blobs(prefix='stored_codes/python/')
        
        self.assertEqual(len(blobs), 2)
        self.assertEqual(blobs[0]['pathname'], 'stored_codes/python/file1.py')
    
    @patch('blob_storage.requests.get')
    def test_list_blobs_empty(self, mock_get):
        """Test listing blobs when none exist"""
        # Mock empty response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'blobs': []}
        mock_get.return_value = mock_response
        
        client = VercelBlobStorage(self.test_token)
        blobs = client.list_blobs()
        
        self.assertEqual(len(blobs), 0)
    
    def test_blob_client_disabled_without_token(self):
        """Test that operations fail gracefully when client is disabled"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                client = VercelBlobStorage()


class TestBlobStorageIntegration(unittest.TestCase):
    """Integration tests for blob storage with Flask app"""
    
    @patch.dict(os.environ, {'BLOB_READ_WRITE_TOKEN': 'test_token'}, clear=False)
    @patch('blob_storage.VercelBlobStorage')
    def test_blob_client_created_when_enabled(self, mock_blob_class):
        """Test that blob client is created when token is configured"""
        # This would test the actual Flask app integration
        # For now, just verify the module functions work
        self.assertTrue(is_blob_storage_enabled())
        
        client = get_blob_client()
        self.assertIsNotNone(client)


if __name__ == '__main__':
    unittest.main()
