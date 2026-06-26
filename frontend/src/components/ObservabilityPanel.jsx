const getValue = (...values) => values.find((value) => value !== undefined && value !== null && value !== '');

const ObservabilityPanel = ({ observability, result }) => {
  const monitoring = result?.monitoring || {};
  const aiSafety = result?.report?.ai_safety || monitoring.ai_safety || {};
  const finalDecision = aiSafety.final_decision || {};
  const langsmith = monitoring.langsmith || {};

  const items = [
    ['correlation_id', getValue(result?.correlation_id, langsmith.correlation_id)],
    ['decision', getValue(result?.decision, finalDecision.action)],
    ['risk_level', getValue(result?.risk_level, result?.report?.risk_analysis?.risk_level)],
    ['execution_time_ms', getValue(monitoring.execution_time_ms, monitoring.latency_ms)],
    ['logs_enabled', getValue(monitoring.observability?.logs_enabled, observability?.logs_enabled)],
    ['metrics_enabled', getValue(monitoring.observability?.metrics_enabled, observability?.metrics_enabled)],
    ['correlation_id_enabled', getValue(monitoring.observability?.correlation_id_enabled, observability?.correlation_id_enabled)],
    ['langsmith trace status', getValue(langsmith.trace_available, observability?.langsmith_enabled, observability?.enabled)],
  ];

  return (
    <section className="card">
      <div className="section-header">
        <div>
          <h2>Observability</h2>
          <p className="text-muted">Correlation, telemetry flags and trace status.</p>
        </div>
      </div>
      <div className="detail-grid">
        {items.map(([label, value]) => (
          <div key={label}>
            <span>{label}</span>
            <strong>{value === undefined ? 'N/A' : String(value)}</strong>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ObservabilityPanel;
