import { Fragment } from 'react';

const workflowNodes = [
  { name: 'Client', role: 'Incident submission', icon: '👤' },
  { name: 'FastAPI', role: 'API gateway', icon: '⚡' },
  { name: 'Supervisor Agent', role: 'LangGraph orchestration', icon: '🧠' },
  { name: 'Risk Agent', role: 'Financial risk scoring', icon: '📊' },
  { name: 'Fraud Agent', role: 'Fraud signal detection', icon: '🕵️' },
  { name: 'Compliance Agent', role: 'AML/KYC checks', icon: '⚖️' },
  { name: 'Monitoring Agent', role: 'Telemetry and safety', icon: '📡' },
  { name: 'Report', role: 'Final decision', icon: '📄' },
];

const AgentWorkflow = ({ status = 'pending' }) => {
  const normalizedStatus = ['pending', 'running', 'completed', 'error'].includes(status)
    ? status
    : 'pending';

  return (
    <section className="card">
      <div className="section-header">
        <div>
          <h2>LangGraph Workflow</h2>
          <p className="text-muted">Multi-agent orchestration from intake to final report.</p>
        </div>
        <span className={`badge badge-${normalizedStatus}`}>{normalizedStatus}</span>
      </div>

      <div className="workflow">
        {workflowNodes.map((node, index) => (
          <Fragment key={node.name}>
            <div className={`workflow-node workflow-${normalizedStatus}`}>
              <div className="workflow-icon">{node.icon}</div>
              <div>
                <h3>{node.name}</h3>
                <p>{node.role}</p>
              </div>
              <span className={`badge badge-${normalizedStatus}`}>{normalizedStatus}</span>
            </div>
            {index < workflowNodes.length - 1 && <div className="workflow-arrow">↓</div>}
          </Fragment>
        ))}
      </div>
    </section>
  );
};

export default AgentWorkflow;
