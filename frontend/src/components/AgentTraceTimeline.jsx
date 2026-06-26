const getValue = (...values) => values.find((value) => value !== undefined && value !== null && value !== '');

const AgentTraceTimeline = ({ result, status = 'pending' }) => {
  const correlationId = getValue(result?.correlation_id, result?.monitoring?.correlation_id, 'pending');
  const decision = getValue(result?.decision, result?.report?.final_status, 'pending');
  const riskLevel = getValue(result?.risk_level, result?.report?.risk_analysis?.risk_level, 'pending');

  const steps = [
    { title: 'correlation_id generated', detail: correlationId },
    { title: 'Supervisor started', detail: 'LangGraph state initialized' },
    { title: 'Risk Agent completed', detail: riskLevel },
    { title: 'Fraud Agent completed', detail: getValue(result?.fraud_suspicion, result?.report?.fraud_analysis?.fraud_suspicion, 'pending') },
    { title: 'Compliance Agent completed', detail: getValue(result?.compliance_status, result?.report?.compliance_analysis?.compliance_status, 'pending') },
    { title: 'Monitoring completed', detail: getValue(result?.monitoring?.status, result?.report?.ai_safety?.safe, 'pending') },
    { title: 'Report generated', detail: result?.report ? 'available' : 'pending' },
    { title: 'Final decision', detail: decision },
  ];

  const completed = status === 'completed';

  return (
    <section className="card">
      <div className="section-header">
        <div>
          <h2>Agent Trace Timeline</h2>
          <p className="text-muted">Execution trace reconstructed from the analysis response.</p>
        </div>
      </div>
      <div className="timeline">
        {steps.map((step, index) => (
          <div className="timeline-item" key={step.title}>
            <div className={`timeline-dot ${completed ? 'timeline-done' : status === 'running' && index <= 1 ? 'timeline-running' : ''}`} />
            <div>
              <h3>{step.title}</h3>
              <p>{String(step.detail)}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default AgentTraceTimeline;
