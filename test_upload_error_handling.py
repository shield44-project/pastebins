"""
Test error handling in file upload endpoints
"""
import pytest
import tempfile
import os
import json
from app import app
from io import BytesIO


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['CODES_DIRECTORY'] = tempfile.mkdtemp()
    with app.test_client() as client:
        yield client


def test_upload_no_files(client):
    """Test upload with no files provided"""
    response = client.post('/upload-files', data={
        'language': 'python'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'No files' in data['error']


def test_upload_invalid_language(client):
    """Test upload with invalid language"""
    data = {
        'files': (BytesIO(b'print("hello")'), 'test.py'),
        'language': 'invalid_language'
    }
    response = client.post('/upload-files', data=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid language' in data['error']


def test_upload_no_files_selected(client):
    """Test upload with empty file list"""
    response = client.post('/upload-files', data={
        'language': 'python',
        'files': []
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_upload_encryption_without_password(client):
    """Test upload with encryption enabled but no password"""
    data = {
        'files': (BytesIO(b'print("hello")'), 'test.py'),
        'language': 'python',
        'encrypt': 'on'
    }
    response = client.post('/upload-files', data=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Password is required' in data['error']


def test_upload_code_no_title(client):
    """Test code upload without title"""
    response = client.post('/upload', data={
        'language': 'python',
        'code': 'print("hello")'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'required' in data['error'].lower()


def test_upload_code_no_content(client):
    """Test code upload without content"""
    response = client.post('/upload', data={
        'language': 'python',
        'title': 'Test Code'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'required' in data['error'].lower()


def test_upload_code_invalid_title(client):
    """Test code upload with invalid title containing path separators"""
    response = client.post('/upload', data={
        'language': 'python',
        'title': '../test',
        'code': 'print("hello")'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid title' in data['error']


def test_upload_wrong_extension(client):
    """Test upload with wrong file extension"""
    data = {
        'files': (BytesIO(b'print("hello")'), 'test.java'),
        'language': 'python'
    }
    response = client.post('/upload-files', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_upload_invalid_filename(client):
    """Test upload with invalid filename characters"""
    data = {
        'files': (BytesIO(b'print("hello")'), 'test<>.py'),
        'language': 'python'
    }
    response = client.post('/upload-files', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_error_handler_413():
    """Test that 413 error handler is registered"""
    with app.test_client() as client:
        # This tests that the error handler exists
        # We can't easily trigger a 413 in a unit test without mocking
        assert 413 in app.error_handler_spec[None]


def test_error_handler_500():
    """Test that 500 error handler is registered"""
    with app.test_client() as client:
        # This tests that the error handler exists
        assert 500 in app.error_handler_spec[None]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
