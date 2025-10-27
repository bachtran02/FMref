import React from 'react';
import FileUpload from './components/FileUpload'; // Import the component
import './App.css'; // Default styling from Vite

function App(): JSX.Element {
  // Define your backend API base URL (adjust if needed)
  // Use environment variables in a real app for flexibility
  const API_BASE_URL: string = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';

  return (
    <div className="App">
      <header className="App-header">
        <h1>Football Manager Analyzer ⚽</h1>
        {/* You might add navigation or user info here later */}
      </header>
      <main className="App-main">
        <div className="upload-section">
          {/* Component for uploading Player data */}
          <FileUpload
             label="Player Data"
             uploadUrl={`${API_BASE_URL}/upload_players`}
          />
        </div>

        <hr className="separator" /> {/* Simple separator */}

        <div className="upload-section">
          {/* Component for uploading Team data */}
          <FileUpload
             label="Team Data"
             uploadUrl={`${API_BASE_URL}/upload_teams`}
           />
        </div>

        {/* Placeholder for where results/visualizations might go */}
        <div className="results-section">
          {/* Results components will go here */}
        </div>
      </main>
      <footer className="App-footer">
        <p>Built with React, TypeScript, Vite, and Flask</p>
      </footer>
    </div>
  );
}

export default App;