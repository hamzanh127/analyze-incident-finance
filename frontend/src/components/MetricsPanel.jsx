const MetricsPanel = ({ metrics, loading, error }) => {
  const items = [
    ['total_requests', metrics?.total_requests ?? 0],
    ['total_errors', metrics?.total_errors ?? 0],
    ['total_high_risk', metrics?.total_high_risk ?? 0],
    ['total_manual_review', metrics?.total_manual_review ?? 0],
    ['total_blocked', metrics?.total_blocked ?? 0],
    ['average_latency_ms', metrics?.average_latency_ms !== undefined ? `${metrics.average_latency_ms} ms` : 'N/A'],
  ];

  return (
    <section className="card">
      <div className="section-header">
        <div>
          <h2>Metrics</h2>
          <p className="text-muted">Live counters exposed by the backend.</p>
        </div>
        {loading && <span className="loading-spinner" />}
      </div>
      {error && <div className="notice notice-warning">{error}</div>}
      <div className="metric-grid">
        {items.map(([label, value]) => (
          <div className="metric-item" key={label}>
            <span className="metric-label">{label}</span>
            <span className="metric-value">{value}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

export default MetricsPanel;
