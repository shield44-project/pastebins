import React from 'react';

interface HeaderProps {
  onOpenUpload: () => void;
  onOpenNotes: () => void;
}

const Header: React.FC<HeaderProps> = ({ onOpenUpload, onOpenNotes }) => {
  return (
    <header>
      <h1>💻 NeonBin - Matrix Code Vault</h1>
      <p className="subtitle">The ultimate code storage platform with neon aesthetics and advanced encryption</p>
      
      {/* Navigation Bar */}
      <div style={{ textAlign: 'center', marginBottom: '20px', padding: '15px', background: 'rgba(0, 255, 0, 0.05)', borderRadius: '10px', border: '1px solid rgba(0, 255, 0, 0.2)' }}>
        <a href="upload_standalone.html" style={{ color: '#00ff00', fontSize: '1.2em', fontWeight: 600, textDecoration: 'none', textShadow: '0 0 10px rgba(0, 255, 0, 0.5)', transition: 'all 0.3s', marginRight: '20px' }}>
          📤 Upload Code
        </a>
        <button onClick={onOpenNotes} style={{ color: '#00ff00', fontSize: '1.2em', fontWeight: 600, background: 'none', border: 'none', cursor: 'pointer', textShadow: '0 0 10px rgba(0, 255, 0, 0.5)', transition: 'all 0.3s' }}>
          📝 Notes
        </button>
      </div>
      
      <div className="btn-group">
        <button onClick={onOpenUpload} className="btn btn-primary">📤 Upload Code</button>
        <button onClick={onOpenNotes} className="btn btn-primary">📝 Create Note</button>
        <a href="viewer.html" className="btn btn-primary">🔐 Open Encrypted File Viewer</a>
        <a href="https://github.com/shield44-project/pastebins" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">📂 View on GitHub</a>
      </div>
    </header>
  );
};

export default Header;
