const normalizeBadge = (value) => {
  const normalized = String(value ?? '').toLowerCase();
  if (['safe', 'allow', 'allowed', 'clean', 'none', 'false'].includes(normalized)) return 'badge-success';
  if (['warning', 'sanitize', 'manual_review', 'review', 'medium'].includes(normalized)) return 'badge-warning';
  if (['blocked', 'block', 'detected', 'unsafe', 'true', 'high'].includes(normalized)) return 'badge-danger';
  return 'badge-default';
};

const asLabel = (value, fallback = 'N/A') => (
  value === undefined || value === null || value === '' ? fallback : String(value)
);

const pickSafety = (result) => (
  result?.report?.ai_safety || result?.monitoring?.ai_safety || result?.ai_safety || null
);

const MonitoringPanel = ({ result }) => {
  const safety = pickSafety(result);
  const monitoring = result?.monitoring || {};

  if (!result && !safety) return null;

  const staticChecks = safety?.static_checks || safety || {};
  const grokReview = safety?.grok_safety_review || {};
  const finalDecision = safety?.final_decision || {};

  const toxicity = staticChecks.toxicity?.status || staticChecks.toxicity?.detected || monitoring.toxicity_detected;
  const promptInjection = staticChecks.prompt_injection?.detected ?? monitoring.prompt_injection_detected;
  const pii = staticChecks.pii?.detected ?? monitoring.pii_detected;
  const tokens = staticChecks.tokens?.estimated_tokens ?? staticChecks.tokens?.total ?? monitoring.token_count;
  const cost = staticChecks.cost?.estimated_cost ?? staticChecks.cost?.total ?? monitoring.cost;
  const finalAction = finalDecision.action || (safety?.safe === false ? 'block' : 'allow');
  const finalSafe = finalDecision.safe ?? safety?.safe;

  const rows = [
    ['Static Toxicity', toxicity ? asLabel(toxicity) : 'clean'],
    ['Static Prompt Injection', promptInjection ? 'detected' : 'clean'],
    ['Static PII', pii ? 'detected' : 'none'],
    ['Grok Overall Risk', grokReview.overall_risk || (grokReview.available === false ? 'unavailable' : 'N/A')],
    ['Grok Recommended Action', grokReview.recommended_action || 'N/A'],
    ['Final Safety Decision', `${asLabel(finalAction)}${finalSafe === false ? ' / unsafe' : finalSafe === true ? ' / safe' : ''}`],
    ['Tokens', asLabel(tokens)],
    ['Cost', cost === undefined || cost === null ? 'N/A' : `$${Number(cost).toFixed(6)}`],
  ];

  return (
    <section className="card">
      <div className="section-header">
        <div>
          <h2>Monitoring Security</h2>
          <p className="text-muted">AI safety checks, token telemetry and cost estimate.</p>
        </div>
        <span className={`badge ${normalizeBadge(finalAction)}`}>{asLabel(finalAction)}</span>
      </div>
      <div className="monitoring-list">
        {rows.map(([label, value]) => (
          <div className="monitoring-row" key={label}>
            <span>{label}</span>
            <strong className={`badge ${normalizeBadge(value)}`}>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
};

export default MonitoringPanel;
