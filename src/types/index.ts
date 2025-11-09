// Type definitions for the application

export interface CodeFile {
  id: string;
  language: ProgrammingLanguage;
  title: string;
  description?: string;
  code: string;
  created: string;
}

export type ProgrammingLanguage = 
  | 'python' 
  | 'java' 
  | 'c' 
  | 'cpp' 
  | 'javascript' 
  | 'typescript' 
  | 'react' 
  | 'html';

export interface Feature {
  icon: string;
  title: string;
  description: string;
}

export interface Language {
  emoji: string;
  name: string;
  code: ProgrammingLanguage;
}

export interface UploadFormData {
  language: ProgrammingLanguage;
  title: string;
  description?: string;
  code?: string;
  file?: File;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
