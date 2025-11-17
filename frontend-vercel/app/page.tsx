'use client';

import { useState } from 'react';

type Language = 'c' | 'cpp' | 'python';

interface RunResult {
  stdout: string;
  stderr: string;
  error: string | null;
  success: boolean;
  compilation_info?: string;
}

export default function Home() {
  const [language, setLanguage] = useState<Language>('c');
  const [code, setCode] = useState<string>('');
  const [input, setInput] = useState<string>('');
  const [output, setOutput] = useState<RunResult | null>(null);
  const [isRunning, setIsRunning] = useState<boolean>(false);

  const sampleCode: Record<Language, string> = {
    c: `#include <stdio.h>

int main() {
    printf("Hello from C!\\n");
    return 0;
}`,
    cpp: `#include <iostream>
using namespace std;

int main() {
    cout << "Hello from C++!" << endl;
    return 0;
}`,
    python: `print("Hello from Python!")`
  };

  const handleLanguageChange = (newLang: Language) => {
    setLanguage(newLang);
    if (!code || code === sampleCode[language]) {
      setCode(sampleCode[newLang]);
    }
  };

  const handleRun = async () => {
    setIsRunning(true);
    setOutput(null);

    try {
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000';
      
      const response = await fetch(`${backendUrl}/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          language,
          code,
          input,
        }),
      });

      const result: RunResult = await response.json();
      setOutput(result);
    } catch (error) {
      setOutput({
        stdout: '',
        stderr: '',
        error: `Failed to connect to backend: ${error instanceof Error ? error.message : 'Unknown error'}`,
        success: false,
      });
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-700 bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
            Online Code Runner
          </h1>
          <p className="text-gray-400 mt-1">
            Compile and run C, C++, and Python code online
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Code Editor */}
          <div className="space-y-4">
            {/* Language Selector */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Select Language
              </label>
              <select
                value={language}
                onChange={(e) => handleLanguageChange(e.target.value as Language)}
                className="w-full bg-gray-700 border border-gray-600 rounded-md px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="c">C</option>
                <option value="cpp">C++</option>
                <option value="python">Python</option>
              </select>
            </div>

            {/* Code Editor */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Code
              </label>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder={`Write your ${language.toUpperCase()} code here...`}
                className="w-full h-96 bg-gray-900 border border-gray-600 rounded-md px-4 py-3 text-white font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                spellCheck={false}
              />
            </div>

            {/* Input */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Input (stdin)
              </label>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Enter input for your program (optional)"
                className="w-full h-24 bg-gray-900 border border-gray-600 rounded-md px-4 py-3 text-white font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>

            {/* Run Button */}
            <button
              onClick={handleRun}
              disabled={isRunning || !code.trim()}
              className={`w-full py-3 px-6 rounded-lg font-medium text-lg transition-all duration-200 ${
                isRunning || !code.trim()
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl'
              }`}
            >
              {isRunning ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Running...
                </span>
              ) : (
                '▶️ Run Code'
              )}
            </button>
          </div>

          {/* Right Panel - Output */}
          <div className="space-y-4">
            {/* Output Display */}
            {output && (
              <>
                {/* Success/Error Banner */}
                <div className={`rounded-lg p-4 border ${
                  output.success
                    ? 'bg-green-900/30 border-green-700 text-green-300'
                    : 'bg-red-900/30 border-red-700 text-red-300'
                }`}>
                  <div className="flex items-center">
                    <span className="text-2xl mr-2">
                      {output.success ? '✅' : '❌'}
                    </span>
                    <div>
                      <p className="font-semibold">
                        {output.success ? 'Execution Successful' : 'Execution Failed'}
                      </p>
                      {output.compilation_info && (
                        <p className="text-sm mt-1 opacity-90">{output.compilation_info}</p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Standard Output */}
                {output.stdout && (
                  <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                    <h3 className="text-sm font-medium text-green-400 mb-2 flex items-center">
                      <span className="mr-2">📤</span>
                      Standard Output (stdout)
                    </h3>
                    <pre className="bg-gray-900 rounded p-3 text-green-300 font-mono text-sm overflow-x-auto whitespace-pre-wrap break-words">
                      {output.stdout}
                    </pre>
                  </div>
                )}

                {/* Standard Error / Compilation Info */}
                {output.stderr && (
                  <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                    <h3 className="text-sm font-medium text-yellow-400 mb-2 flex items-center">
                      <span className="mr-2">⚠️</span>
                      {output.success ? 'Warnings' : 'Errors / Compilation Output'}
                    </h3>
                    <pre className="bg-gray-900 rounded p-3 text-yellow-300 font-mono text-sm overflow-x-auto whitespace-pre-wrap break-words">
                      {output.stderr}
                    </pre>
                  </div>
                )}

                {/* Error Message */}
                {output.error && (
                  <div className="bg-gray-800 rounded-lg p-4 border border-red-700">
                    <h3 className="text-sm font-medium text-red-400 mb-2 flex items-center">
                      <span className="mr-2">🚫</span>
                      Error
                    </h3>
                    <p className="text-red-300 font-mono text-sm">
                      {output.error}
                    </p>
                  </div>
                )}
              </>
            )}

            {/* Initial State */}
            {!output && !isRunning && (
              <div className="bg-gray-800 rounded-lg p-8 border border-gray-700 text-center">
                <div className="text-6xl mb-4">🚀</div>
                <h3 className="text-xl font-semibold text-gray-300 mb-2">
                  Ready to Run
                </h3>
                <p className="text-gray-400">
                  Write your code and click the Run button to see the output here
                </p>
              </div>
            )}

            {/* Running State */}
            {isRunning && (
              <div className="bg-gray-800 rounded-lg p-8 border border-gray-700 text-center">
                <div className="text-6xl mb-4 animate-pulse">⚡</div>
                <h3 className="text-xl font-semibold text-gray-300 mb-2">
                  Executing Code...
                </h3>
                <p className="text-gray-400">
                  Please wait while your code is being compiled and executed
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 bg-gray-800/50 rounded-lg p-6 border border-gray-700">
          <h3 className="text-lg font-semibold mb-3 text-blue-400">🔧 Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
            <div>
              <strong className="text-white">Intelligent Compilation:</strong>
              <p className="text-gray-400 mt-1">
                Automatically tries multiple compiler strategies until your code runs
              </p>
            </div>
            <div>
              <strong className="text-white">Zero Warnings:</strong>
              <p className="text-gray-400 mt-1">
                All compiler warnings are automatically suppressed
              </p>
            </div>
            <div>
              <strong className="text-white">AI Suggestions:</strong>
              <p className="text-gray-400 mt-1">
                Get helpful hints when compilation fails
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-700 bg-gray-900/50 backdrop-blur-sm mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-gray-400">
          <p>Online Code Runner - Deploy on Vercel (Frontend) + Railway/Render (Backend)</p>
        </div>
      </footer>
    </div>
  );
}

