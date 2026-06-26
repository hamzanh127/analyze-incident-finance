import React from 'react';
import AgentCard from './AgentCard';
import MonitoringPanel from './MonitoringPanel';

const ResultDashboard = ({ result }) => {
  if (!result) return null;

  return (
    <div style={{ marginTop: '2rem' }}>
      <div className="card text-center" style={{ backgroundColor: '#e9ecef', borderColor: '#dee2e6' }}>
        <h2 style={{ marginBottom: '0.5rem' }}>Final Decision: <span className={`badge ${result.decision === 'APPROVE' ? 'badge-success' : result.decision === 'REJECT' ? 'badge-danger' : 'badge-warning'}`} style={{ fontSize: '1.5rem' }}>{result.decision}</span></h2>
        <p className="text-muted">Correlation ID: {result.correlation_id}</p>
      </div>

      <div className="pipeline">
        <div className="pipeline-step">Supervisor</div>
        <div className="pipeline-arrow">→</div>
        <div className="pipeline-step">Risk</div>
        <div className="pipeline-arrow">→</div>
        <div className="pipeline-step">Fraud</div>
        <div className="pipeline-arrow">→</div>
        <div className="pipeline-step">Compliance</div>
        <div className="pipeline-arrow">→</div>
        <div className="pipeline-step">Monitoring</div>
        <div className="pipeline-arrow">→</div>
        <div className="pipeline-step">Final Report</div>
      </div>

      <div className="grid-2">
        <AgentCard 
          title="Risk Agent" 
          statusText={result.risk_level} 
          statusLevel={result.risk_level}
          details={`Risk Score: ${result.risk_score}/100`} 
        />
        <AgentCard 
          title="Fraud Agent" 
          statusText={result.fraud_suspicion ? 'Suspicious' : 'Clean'} 
          statusLevel={result.fraud_suspicion ? 'High' : 'Low'}
          details={`Fraud Score: ${result.fraud_score}/100`} 
        />
        <AgentCard 
          title="Compliance Agent" 
          statusText={result.compliance_status} 
          statusLevel={result.compliance_status}
          details="All necessary checks performed." 
        />
        <AgentCard 
          title="Recommendations" 
          details={result.recommendations?.length > 0 ? result.recommendations : "No specific recommendations."} 
        />
      </div>

      <MonitoringPanel monitoring={result.monitoring} />

      {result.report && (
        <div className="card" style={{ marginTop: '1.5rem' }}>
          <h2>Detailed Report</h2>
          <div className="pre-wrap">
            {JSON.stringify(result.report, null, 2)}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDashboard;
