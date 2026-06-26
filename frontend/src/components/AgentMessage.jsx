import React from 'react';

const AgentMessage = ({ agentName, avatar, statusLevel, statusText, content, details }) => {
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
      case 'review_required':
        return 'badge-warning';
      case 'Low':
      case 'low':
      case 'APPROVE':
      case 'Pass':
      case false:
      case 'compliant':
        return 'badge-success';
      default:
        return 'badge-default';
    }
  };

  return (
    <div className="chat-message animate-fade-in">
      <div className="chat-avatar">{avatar}</div>
      <div className="chat-content-wrapper">
        <div className="chat-header">
          <span className="chat-agent-name">{agentName}</span>
          {statusText !== undefined && (
            <span className={`badge ${getBadgeClass(statusLevel)}`}>
              {statusText}
            </span>
          )}
        </div>
        <div className="chat-bubble">
          {content && <p className="chat-main-content">{content}</p>}
          {details && (
            <div className="chat-details text-muted">
              {Array.isArray(details) ? (
                <ul className="chat-details-list">
                  {details.map((d, i) => <li key={i}>{d}</li>)}
                </ul>
              ) : (
                <p>{details}</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentMessage;
