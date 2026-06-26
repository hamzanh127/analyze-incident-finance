const badgeClass = (value) => {
  const normalized = String(value ?? '').toLowerCase();
  if (['approved', 'approve', 'completed', 'low', 'safe', 'false'].includes(normalized)) return 'badge-success';
  if (['manual_review', 'investigate', 'medium', 'review_required'].includes(normalized)) return 'badge-warning';
  if (['blocked', 'reject', 'rejected', 'high', 'true'].includes(normalized)) return 'badge-danger';
  return 'badge-default';
};

const ValueBlock = ({ title, children }) => (
  <div className="result-block">
    <h3>{title}</h3>
    {typeof children === 'string' || typeof children === 'number' ? <p>{children}</p> : children}
  </div>
);

const JsonBlock = ({ value }) => (
  <pre className="pre-wrap">{JSON.stringify(value || {}, null, 2)}</pre>
);

const ResultDashboard = ({ result }) => {
  if (!result) return null;

  const report = result.report || {};
  const summary = report.summary || result.summary || 'Finance incident analysis completed.';
  const finalStatus = report.final_status || result.final_status || 'completed';
  const recommendations = result.recommendations || report.recommended_next_steps || [];

  return (
    <section className="card">
      <div className="decision-banner">
        <div>
          <span className="eyebrow">Final decision</span>
          <h2>{result.decision || 'N/A'}</h2>
          <p>Correlation ID: {result.correlation_id || 'N/A'}</p>
        </div>
        <span className={`badge ${badgeClass(result.decision)}`}>{result.decision || 'unknown'}</span>
      </div>

      <div className="result-grid">
        <ValueBlock title="Summary">{summary}</ValueBlock>
        <ValueBlock title="Decision">
          <span className={`badge ${badgeClass(result.decision)}`}>{result.decision || 'N/A'}</span>
        </ValueBlock>
        <ValueBlock title="Final Status">
          <span className={`badge ${badgeClass(finalStatus)}`}>{finalStatus}</span>
        </ValueBlock>
        <ValueBlock title="Recommendations">
          {recommendations.length > 0 ? (
            <ul>
              {recommendations.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}
            </ul>
          ) : (
            <p>No specific recommendations.</p>
          )}
        </ValueBlock>
      </div>

      <div className="grid-3">
        <ValueBlock title="Risk Analysis">
          <JsonBlock value={report.risk_analysis || { risk_level: result.risk_level, risk_score: result.risk_score }} />
        </ValueBlock>
        <ValueBlock title="Fraud Analysis">
          <JsonBlock value={report.fraud_analysis || { fraud_suspicion: result.fraud_suspicion, fraud_score: result.fraud_score }} />
        </ValueBlock>
        <ValueBlock title="Compliance Analysis">
          <JsonBlock value={report.compliance_analysis || { compliance_status: result.compliance_status }} />
        </ValueBlock>
      </div>
    </section>
  );
};

export default ResultDashboard;
