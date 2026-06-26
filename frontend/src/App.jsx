import React, { useState } from 'react';
import IncidentForm from './components/IncidentForm';
import AgentChat from './components/AgentChat';
import MetricsPanel from './components/MetricsPanel';
import { analyzeIncident } from './api';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(true);

  const handleAnalyze = async (payload) => {
    setShowForm(false);
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeIncident(payload);
      setResult(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setLoading(false);
    }
  };

  const handleNewIncident = () => {
    setShowForm(true);
    setResult(null);
    setError(null);
  };

  return (
    <div className="container">
      <h1>AI Agents Control Center</h1>
      
      <div className="grid-2">
        <div>
          {showForm ? (
            <IncidentForm onSubmit={handleAnalyze} isLoading={loading} />
          ) : (
            <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ margin: 0 }}>Incident Analysis in Progress</h3>
                <p className="text-muted" style={{ margin: 0, fontSize: '0.9rem' }}>The multi-agent system is working on the case.</p>
              </div>
              <button className="btn btn-primary" onClick={handleNewIncident} style={{ width: 'auto' }}>
                New Incident
              </button>
            </div>
          )}
        </div>
        <div>
          <MetricsPanel />
        </div>
      </div>

      {(!showForm || loading || result || error) && (
        <div style={{ marginTop: '2rem' }}>
          <AgentChat loading={loading} error={error} result={result} />
        </div>
      )}
    </div>
  );
}

export default App;
