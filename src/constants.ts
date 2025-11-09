/**
 * Application constants
 */

export const APP_NAME = 'NeonBin - Matrix Code Vault';
export const APP_DESCRIPTION = 'The ultimate code storage platform with neon aesthetics and advanced encryption';

export const GITHUB_REPO_URL = 'https://github.com/shield44-project/pastebins';

export const SUPPORTED_LANGUAGES = [
  'python',
  'java', 
  'c',
  'cpp',
  'javascript',
  'typescript',
  'react',
  'html'
] as const;

export const LANGUAGE_EXTENSIONS: Record<string, string> = {
  python: '.py',
  java: '.java',
  c: '.c',
  cpp: '.cpp',
  javascript: '.js',
  typescript: '.ts',
  react: '.jsx',
  html: '.html'
};

export const FILE_UPLOAD_MAX_SIZE = 16 * 1024 * 1024; // 16MB

export const CODE_EXECUTION_TIMEOUT = 5000; // 5 seconds

export const LOCAL_STORAGE_KEY = 'pastebin_codes';
