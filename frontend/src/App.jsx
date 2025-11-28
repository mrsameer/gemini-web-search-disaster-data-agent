import React, { useState } from 'react';
import DisasterCard from './components/DisasterCard';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const data = await response.json();
      setResults(data.events || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetch('http://localhost:8000/api/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error('Export failed');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'disaster_data.json';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Disaster Data Agent</h1>
        <p>Real-time global disaster monitoring powered by Gemini</p>
      </div>

      <div className="search-container">
        <form onSubmit={handleSearch}>
          <input
            type="text"
            className="search-input"
            placeholder="Search for disasters (e.g., 'Floods in India last week')..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="search-button" disabled={loading || !query.trim()}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>
      </div>

      {results.length > 0 && (
        <button
          onClick={handleExport}
          className="search-button"
          style={{ marginTop: '1rem', backgroundColor: '#10b981' }}
        >
          Export JSON
        </button>
      )}

      {loading && <div className="loading-spinner"></div>}

      {error && (
        <div style={{ color: '#ef4444', marginTop: '1rem' }}>
          Error: {error}
        </div>
      )}

      <div className="results-grid">
        {results.map((event, index) => (
          <DisasterCard key={index} event={event} />
        ))}
      </div>

      {!loading && results.length === 0 && query && !error && (
        <p style={{ color: 'var(--text-secondary)', marginTop: '2rem' }}>
          No results found. Try a different query.
        </p>
      )}
    </div>
  );
}

export default App;
