import React from 'react';

const MonitoringPanel = ({ monitoring }) => {
  if (!monitoring) return null;

  return (
    <div className="card" style={{ marginTop: '1.5rem' }}>
      <h2>Monitoring & Security</h2>
      <div className="metric-grid">
        <div className="metric-item">
          <span className="metric-label">Latency</span>
          <span className="metric-value">{monitoring.latency_ms !== undefined ? `${monitoring.latency_ms} ms` : 'N/A'}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Token Usage</span>
          <span className="metric-value">{monitoring.token_count !== undefined ? monitoring.token_count : 'N/A'}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Cost</span>
          <span className="metric-value">{monitoring.cost !== undefined ? `$${monitoring.cost.toFixed(4)}` : 'N/A'}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">PII Detected</span>
          <span className="metric-value" style={{ color: monitoring.pii_detected ? 'var(--danger)' : 'var(--success)' }}>
            {monitoring.pii_detected ? 'Yes' : 'No'}
          </span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Prompt Injection</span>
          <span className="metric-value" style={{ color: monitoring.prompt_injection_detected ? 'var(--danger)' : 'var(--success)' }}>
            {monitoring.prompt_injection_detected ? 'Detected' : 'Clean'}
          </span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Toxicity</span>
          <span className="metric-value" style={{ color: monitoring.toxicity_detected ? 'var(--danger)' : 'var(--success)' }}>
            {monitoring.toxicity_detected ? 'High' : 'Low'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default MonitoringPanel;
