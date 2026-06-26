import { useState } from 'react';

const valueOrFallback = (value, fallback = 'N/A') => (
  value === undefined || value === null || value === '' ? fallback : String(value)
);

const LangSmithPanel = ({ observability, result }) => {
  const [copied, setCopied] = useState(false);
  const langsmith = result?.monitoring?.langsmith || result?.report?.langsmith || {};
  const correlationId = result?.correlation_id || langsmith.correlation_id || '';
  const enabled = Boolean(langsmith.enabled ?? observability?.langsmith_enabled ?? observability?.enabled);

  const copyCorrelationId = async () => {
    if (!correlationId) return;
    await navigator.clipboard.writeText(correlationId);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <section className="card">
      <div className="section-header">
        <div>
          <h2>LangSmith</h2>
          <p className="text-muted">External tracing status and current analysis trace metadata.</p>
        </div>
        <span className={`badge ${enabled ? 'badge-success' : 'badge-default'}`}>
          {enabled ? 'enabled' : 'disabled'}
        </span>
      </div>

      {!enabled && (
        <div className="notice">
          LangSmith tracing is disabled. Add LANGSMITH_API_KEY to enable traces.
        </div>
      )}

      <div className="detail-grid">
        <div><span>Project</span><strong>{valueOrFallback(langsmith.project || observability?.project)}</strong></div>
        <div><span>Tracing</span><strong>{valueOrFallback(observability?.tracing ?? observability?.langsmith_tracing)}</strong></div>
        <div><span>Environment</span><strong>{valueOrFallback(observability?.environment)}</strong></div>
        <div><span>Version</span><strong>{valueOrFallback(observability?.version)}</strong></div>
        <div><span>Trace Available</span><strong>{valueOrFallback(langsmith.trace_available)}</strong></div>
        <div><span>Run Name</span><strong>{valueOrFallback(langsmith.run_name)}</strong></div>
        <div><span>Correlation ID</span><strong>{valueOrFallback(correlationId)}</strong></div>
      </div>

      <div className="button-row">
        <button className="btn btn-secondary" type="button" onClick={copyCorrelationId} disabled={!correlationId}>
          {copied ? 'Copied' : 'Copy Correlation ID'}
        </button>
        <a className="btn btn-primary btn-inline" href="https://smith.langchain.com/" target="_blank" rel="noreferrer">
          Open LangSmith Project
        </a>
      </div>
    </section>
  );
};

export default LangSmithPanel;
