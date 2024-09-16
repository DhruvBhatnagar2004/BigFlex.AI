import React, { useState } from 'react';
import './App.css';
import BannerGenerator from './components/BannerGenerator';

function App() {
  const [generatedContent, setGeneratedContent] = useState(null);

  const handleContentGenerated = (content) => {
    setGeneratedContent(content);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered Promotional Content Generator</h1>
      </header>
      <main>
        <BannerGenerator onContentGenerated={handleContentGenerated} />
        {generatedContent && (
          <div className="generated-content">
            <h2>Generated Content</h2>
            {generatedContent.type === 'banner' ? (
              <img src={generatedContent.url} alt="Generated Banner" />
            ) : (
              <video src={generatedContent.url} controls />
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
