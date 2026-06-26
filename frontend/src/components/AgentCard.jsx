import React from 'react';

const AgentCard = ({ title, statusText, statusLevel, details }) => {
  const getBadgeClass = (level) => {
    switch (level) {
      case 'High':
      case 'high':
      case 'REJECT':
      case 'Fail':
      case true:
        return 'badge-danger';
      case 'Medium':
      case 'medium':
      case 'INVESTIGATE':
      case 'Warning':
        return 'badge-warning';
      case 'Low':
      case 'low':
      case 'APPROVE':
      case 'Pass':
      case false:
        return 'badge-success';
      default:
        return 'badge-default';
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ margin: 0, fontSize: '1.25rem' }}>{title}</h3>
        {statusText !== undefined && (
          <span className={`badge ${getBadgeClass(statusLevel)}`}>
            {statusText}
          </span>
        )}
      </div>
      {details && (
        <div className="text-muted" style={{ fontSize: '0.9rem' }}>
          {Array.isArray(details) ? (
            <ul style={{ paddingLeft: '1.5rem', margin: 0 }}>
              {details.map((d, i) => <li key={i}>{d}</li>)}
            </ul>
          ) : (
            <p>{details}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default AgentCard;
