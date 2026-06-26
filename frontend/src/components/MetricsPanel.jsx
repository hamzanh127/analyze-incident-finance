import React, { useEffect, useState } from 'react';
import { getMetrics } from '../api';

const MetricsPanel = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getMetrics();
        setMetrics(data);
        setError(null);
      } catch (err) {
        setError('Failed to load metrics');
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    // Refresh every 10 seconds
    const interval = setInterval(fetchMetrics, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !metrics) {
    return <div className="card text-center"><span className="loading-spinner"></span> Loading metrics...</div>;
  }

  if (error && !metrics) {
    return null; // Silent failure for the panel so it doesn't break the UI
  }

  return (
    <div className="card" style={{ marginTop: '1.5rem', backgroundColor: '#fdfdfe' }}>
      <h2>System Metrics</h2>
      <div className="metric-grid">
        <div className="metric-item">
          <span className="metric-label">Total Requests</span>
          <span className="metric-value">{metrics?.total_requests || 0}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Success Rate</span>
          <span className="metric-value">
            {metrics?.total_requests ? (((metrics.total_requests - (metrics?.error_count || 0)) / metrics.total_requests) * 100).toFixed(1) : 0}%
          </span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Avg Latency</span>
          <span className="metric-value">{metrics?.avg_latency_ms ? `${metrics.avg_latency_ms.toFixed(1)} ms` : 'N/A'}</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">High Risk Incidents</span>
          <span className="metric-value" style={{ color: 'var(--danger)' }}>
            {metrics?.risk_levels?.high || 0}
          </span>
        </div>
      </div>
    </div>
  );
};

export default MetricsPanel;
