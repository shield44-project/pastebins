import React from 'react';
import { Feature } from '../types';

const features: Feature[] = [
  {
    icon: '📁',
    title: 'Code Storage',
    description: 'Upload and organize code files by programming language'
  },
  {
    icon: '👁️',
    title: 'Syntax Highlighting',
    description: 'Beautiful code viewer with syntax highlighting powered by CodeMirror'
  },
  {
    icon: '▶️',
    title: 'Code Execution',
    description: 'Run Python, Java, C, and C++ code directly in the browser'
  },
  {
    icon: '🌐',
    title: 'HTML Preview',
    description: 'Live preview of HTML websites with fullscreen mode'
  },
  {
    icon: '🔐',
    title: 'File Encryption',
    description: 'Secure file encryption with token-based authentication'
  },
  {
    icon: '🗂️',
    title: 'Auto Categorization',
    description: 'Automatic organization by programming language'
  }
];

const FeatureCards: React.FC = () => {
  return (
    <div className="features-grid">
      {features.map((feature, index) => (
        <div key={index} className="feature-card">
          <div className="feature-icon">{feature.icon}</div>
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </div>
      ))}
    </div>
  );
};

export default FeatureCards;
