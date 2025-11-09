import React from 'react';

interface HeaderProps {
  onOpenUpload: () => void;
}

const Header: React.FC<HeaderProps> = ({ onOpenUpload }) => {
  return (
    <header>
      <h1>💻 NeonBin - Matrix Code Vault</h1>
      <p className="subtitle">The ultimate code storage platform with neon aesthetics and advanced encryption</p>
      
      <div className="btn-group">
        <button onClick={onOpenUpload} className="btn btn-primary">📤 Upload Code</button>
        <a href="viewer.html" className="btn btn-primary">🔐 Open Encrypted File Viewer</a>
        <a href="https://github.com/shield44-project/pastebins" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">📂 View on GitHub</a>
      </div>
    </header>
  );
};

export default Header;
