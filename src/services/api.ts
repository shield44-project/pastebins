/**
 * API service for communicating with the Flask backend
 */

import { CodeFile, UploadFormData, ApiResponse } from '../types';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:5000';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      data,
    };
  } catch (error) {
    console.error('API request failed:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Upload a new code file
 */
export async function uploadCode(
  formData: UploadFormData
): Promise<ApiResponse<CodeFile>> {
  return fetchAPI<CodeFile>('/api/upload', {
    method: 'POST',
    body: JSON.stringify(formData),
  });
}

/**
 * Get all code files
 */
export async function getCodeFiles(): Promise<ApiResponse<CodeFile[]>> {
  return fetchAPI<CodeFile[]>('/api/files');
}

/**
 * Get a specific code file by ID
 */
export async function getCodeFile(fileId: string): Promise<ApiResponse<CodeFile>> {
  return fetchAPI<CodeFile>(`/api/files/${fileId}`);
}

/**
 * Delete a code file
 */
export async function deleteCodeFile(fileId: string): Promise<ApiResponse<void>> {
  return fetchAPI<void>(`/api/files/${fileId}`, {
    method: 'DELETE',
  });
}

/**
 * Update a code file
 */
export async function updateCodeFile(
  fileId: string,
  updates: Partial<CodeFile>
): Promise<ApiResponse<CodeFile>> {
  return fetchAPI<CodeFile>(`/api/files/${fileId}`, {
    method: 'PUT',
    body: JSON.stringify(updates),
  });
}

/**
 * Execute code
 */
export async function executeCode(
  language: string,
  code: string,
  input?: string
): Promise<ApiResponse<{ output: string; error?: string }>> {
  return fetchAPI<{ output: string; error?: string }>('/api/execute', {
    method: 'POST',
    body: JSON.stringify({ language, code, input }),
  });
}

/**
 * Get files by language
 */
export async function getFilesByLanguage(
  language: string
): Promise<ApiResponse<CodeFile[]>> {
  return fetchAPI<CodeFile[]>(`/api/files?language=${language}`);
}
