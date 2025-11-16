import React from 'react';
import Header from './components/Header';
import FeatureCards from './components/FeatureCards';
import LanguageBadges from './components/LanguageBadges';
import MatrixRain from './components/MatrixRain';

const App: React.FC = () => {
  const handleOpenUploadModal = (): void => {
    // Upload modal functionality to be implemented
    console.log('Upload modal opened');
  };

  const handleOpenNotesModal = (): void => {
    // Notes modal functionality - redirect to index.html since it has the full implementation
    window.location.href = 'index.html';
  };

  return (
    <>
      <MatrixRain />
      <div className="container">
        <Header onOpenUpload={handleOpenUploadModal} onOpenNotes={handleOpenNotesModal} />
        
        <div className="card">
          <h2 className="section-title">✨ Key Features</h2>
          <FeatureCards />
        </div>

        <div className="card">
          <h2 className="section-title">💻 Supported Languages</h2>
          <LanguageBadges />
        </div>

        <div className="card">
          <h2 className="section-title">🚀 Getting Started</h2>
          
          <div className="info-box">
            <h3>⚠️ Important Note</h3>
            <p><strong>This application requires a Python backend server to run.</strong></p>
            <p>GitHub Pages only supports static HTML/CSS/JavaScript files. To use the full application with code execution features, you need to run it locally.</p>
          </div>

          <h3 style={{ marginTop: '30px', color: '#00ff00' }}>📦 Installation</h3>
          
          <p style={{ margin: '15px 0', color: '#b0b0b0' }}>1. Clone the repository:</p>
          <div className="code-block">
            git clone https://github.com/shield44-project/pastebins.git<br />
            cd pastebins
          </div>

          <p style={{ margin: '15px 0', color: '#b0b0b0' }}>2. Install dependencies:</p>
          <div className="code-block">pip install -r requirements.txt</div>

          <p style={{ margin: '15px 0', color: '#b0b0b0' }}>3. Run the Flask application:</p>
          <div className="code-block">python app.py</div>

          <p style={{ margin: '15px 0', color: '#b0b0b0' }}>4. Open your browser and navigate to:</p>
          <div className="code-block">http://localhost:5000</div>

          <h3 style={{ marginTop: '30px', color: '#00ff00' }}>🔐 Using the Encrypted File Viewer (Static Page)</h3>
          <p style={{ margin: '15px 0', color: '#b0b0b0' }}>
            The <a href="viewer.html" style={{ color: '#00ff00', textDecoration: 'none', fontWeight: 600 }}>Encrypted File Viewer</a> is a standalone static HTML page that can be used on GitHub Pages. It requires a separate decryption server to be running.
          </p>
        </div>

        <div className="card">
          <h2 className="section-title">🛠️ Tech Stack</h2>
          
          <div className="tech-stack">
            <span className="tech-badge">Flask</span>
            <span className="tech-badge">Python 3</span>
            <span className="tech-badge">HTML5</span>
            <span className="tech-badge">CSS3</span>
            <span className="tech-badge">JavaScript</span>
            <span className="tech-badge">TypeScript</span>
            <span className="tech-badge">React</span>
            <span className="tech-badge">Node.js</span>
            <span className="tech-badge">CodeMirror</span>
            <span className="tech-badge">Cryptography</span>
          </div>
        </div>

        <footer>
          <p>Made with ❤️ by shield44-project</p>
          <p style={{ marginTop: '10px', fontSize: '0.9em' }}>
            <a href="https://github.com/shield44-project/pastebins" style={{ color: 'white', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer">
              ⭐ Star us on GitHub
            </a>
          </p>
        </footer>
      </div>
    </>
  );
};

export default App;
