/**
 * Storage utility for managing code files in localStorage
 */

import { CodeFile } from '../types';

const STORAGE_KEY = 'pastebin_codes';

/**
 * Get all stored code files from localStorage
 */
export const getStoredFiles = (): CodeFile[] => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Error reading from localStorage:', error);
    return [];
  }
};

/**
 * Save a code file to localStorage
 */
export const saveFile = (fileData: Omit<CodeFile, 'id' | 'created'>): void => {
  try {
    const files = getStoredFiles();
    const newFile: CodeFile = {
      ...fileData,
      id: Date.now().toString(),
      created: new Date().toISOString()
    };
    files.push(newFile);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(files));
  } catch (error) {
    console.error('Error saving to localStorage:', error);
    throw new Error('Failed to save file');
  }
};

/**
 * Delete a code file from localStorage
 */
export const deleteFile = (fileId: string): void => {
  try {
    const files = getStoredFiles();
    const filtered = files.filter(f => f.id !== fileId);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
  } catch (error) {
    console.error('Error deleting from localStorage:', error);
    throw new Error('Failed to delete file');
  }
};

/**
 * Get a single code file by ID
 */
export const getFileById = (fileId: string): CodeFile | undefined => {
  const files = getStoredFiles();
  return files.find(f => f.id === fileId);
};

/**
 * Update an existing code file
 */
export const updateFile = (fileId: string, updates: Partial<CodeFile>): void => {
  try {
    const files = getStoredFiles();
    const index = files.findIndex(f => f.id === fileId);
    if (index === -1) {
      throw new Error('File not found');
    }
    files[index] = { ...files[index], ...updates };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(files));
  } catch (error) {
    console.error('Error updating file:', error);
    throw new Error('Failed to update file');
  }
};
