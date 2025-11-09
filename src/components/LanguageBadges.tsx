import React from 'react';
import { Language } from '../types';

const languages: Language[] = [
  { emoji: '🐍', name: 'Python', code: 'python' },
  { emoji: '☕', name: 'Java', code: 'java' },
  { emoji: '©️', name: 'C', code: 'c' },
  { emoji: '⚙️', name: 'C++', code: 'cpp' },
  { emoji: '📜', name: 'JavaScript', code: 'javascript' },
  { emoji: '🔷', name: 'TypeScript', code: 'typescript' },
  { emoji: '⚛️', name: 'React', code: 'react' },
  { emoji: '🌐', name: 'HTML', code: 'html' }
];

const LanguageBadges: React.FC = () => {
  return (
    <div className="languages-grid">
      {languages.map((language, index) => (
        <div key={index} className="language-badge">
          {language.emoji} {language.name}
        </div>
      ))}
    </div>
  );
};

export default LanguageBadges;
