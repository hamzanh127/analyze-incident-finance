import React, { useState, useEffect, useRef } from 'react';
import AgentMessage from './AgentMessage';

const AgentChat = ({ loading, error, result }) => {
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  // Scroll to bottom
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Initial message when loading starts
  useEffect(() => {
    if (loading) {
      setMessages([{
        id: 'start',
        agentName: 'Supervisor Agent',
        avatar: '🧠',
        content: 'Analysis started. Coordinating with specialized agents...'
      }]);
    }
  }, [loading]);

  // Handle errors
  useEffect(() => {
    if (error) {
      setMessages(prev => [...prev, {
        id: 'error',
        agentName: 'System',
        avatar: '❌',
        statusLevel: 'High',
        statusText: 'Error',
        content: error
      }]);
    }
  }, [error]);

  // Progressive display when result arrives
  useEffect(() => {
    if (result && !loading && !error) {
      let step = 0;
      
      const sequence = [
        {
          id: 'sup_done',
          agentName: 'Supervisor Agent',
          avatar: '🧠',
          content: `Correlation ID reçu: ${result.correlation_id}`
        },
        {
          id: 'risk',
          agentName: 'Risk Agent',
          avatar: '📊',
          statusLevel: result.risk_level || result.risk_analysis?.risk_level,
          statusText: (result.risk_level || result.risk_analysis?.risk_level || 'Unknown').toUpperCase(),
          content: `Risk Score: ${result.risk_score !== undefined ? result.risk_score : result.risk_analysis?.risk_score}/100`,
          details: result.risk_analysis?.reasons || []
        },
        {
          id: 'fraud',
          agentName: 'Fraud Agent',
          avatar: '🕵️',
          statusLevel: (result.fraud_suspicion !== undefined ? result.fraud_suspicion : result.fraud_analysis?.fraud_suspicion) ? 'High' : 'Low',
          statusText: (result.fraud_suspicion !== undefined ? result.fraud_suspicion : result.fraud_analysis?.fraud_suspicion) ? 'Suspicious' : 'Clean',
          content: `Fraud Score: ${result.fraud_score !== undefined ? result.fraud_score : result.fraud_analysis?.fraud_score}/100`,
          details: result.fraud_analysis?.signals || []
        },
        {
          id: 'compliance',
          agentName: 'Compliance Agent',
          avatar: '⚖️',
          statusLevel: result.compliance_status || result.compliance_analysis?.compliance_status,
          statusText: (result.compliance_status || result.compliance_analysis?.compliance_status || 'Unknown').toUpperCase(),
          content: `Action: ${result.compliance_analysis?.required_action || 'None'}`,
          details: result.compliance_analysis?.reasons || []
        },
        {
          id: 'monitoring',
          agentName: 'Monitoring Agent',
          avatar: '📡',
          ...(() => {
            const aiSafety = result.report?.ai_safety || result.ai_safety || {};
            const staticChecks = aiSafety.static_checks || {};
            const grokReview = aiSafety.grok_safety_review || {};
            const finalDecision = aiSafety.final_decision || {};

            // Static values
            const isToxicityUnsafe = staticChecks.toxicity?.status === 'unsafe';
            const isPromptInjectionDetected = staticChecks.prompt_injection?.detected === true;
            const isPiiDetected = staticChecks.pii?.detected === true;
            const tokens = staticChecks.tokens?.estimated_tokens ?? 'N/A';
            const cost = staticChecks.cost?.estimated_cost !== undefined
              ? `$${Number(staticChecks.cost.estimated_cost).toFixed(6)}`
              : '$0.000000';

            // Grok values
            const grokAvailable = grokReview.available !== false;
            const grokOverallRisk = grokAvailable ? (grokReview.overall_risk || 'safe') : 'N/A';
            const grokAction = grokAvailable ? (grokReview.recommended_action || 'allow') : 'N/A';

            // Final decision
            const finalSafe = finalDecision.safe !== false;
            const finalAction = finalDecision.action || 'allow';
            const finalSource = finalDecision.source || 'static';

            // Badge level
            let statusLevel, statusText;
            if (!finalSafe || finalAction === 'block') {
              statusLevel = 'High';
              statusText = 'Blocked';
            } else if (finalAction === 'manual_review' || finalAction === 'sanitize' || grokOverallRisk === 'warning') {
              statusLevel = 'Medium';
              statusText = 'Warning';
            } else {
              statusLevel = 'Low';
              statusText = 'All Clear';
            }

            return {
              statusLevel,
              statusText,
              content: `Security & Telemetry — Source: ${finalSource}`,
              details: [
                `[Static] Toxicity: ${isToxicityUnsafe ? '🔴 Unsafe' : '🟢 Clean'}`,
                `[Static] Prompt Injection: ${isPromptInjectionDetected ? '🔴 Detected' : '🟢 Clean'}`,
                `[Static] PII: ${isPiiDetected ? '🔴 Detected: ' + (staticChecks.pii?.types || []).join(', ') : '🟢 None'}`,
                `[Grok] Overall Risk: ${grokAvailable ? grokOverallRisk : '⚠️ Unavailable (fallback)'}`,
                `[Grok] Recommended Action: ${grokAvailable ? grokAction : '⚠️ Unavailable'}`,
                `[Final] Decision: ${finalAction.toUpperCase()} (${finalSafe ? '✅ Safe' : '🚫 Not Safe'})`,
                `Tokens: ${tokens}`,
                `Cost: ${cost}`,
              ]
            };
          })()
        },

        {
          id: 'report',
          agentName: 'Final Report',
          avatar: '📄',
          statusLevel: result.decision || result.final_status,
          statusText: (result.decision || result.final_status || 'completed').toUpperCase(),
          content: result.summary || 'Analysis Complete',
          details: result.recommendations || result.recommended_next_steps || []
        }
      ];

      const interval = setInterval(() => {
        if (step < sequence.length) {
          const currentItem = sequence[step];
          setMessages(prev => {
            // Avoid duplicates in React strict mode
            if (!prev.some(m => m.id === currentItem.id)) {
              return [...prev, currentItem];
            }
            return prev;
          });
          step++;
        } else {
          clearInterval(interval);
        }
      }, 800);

      return () => clearInterval(interval);
    }
  }, [result, loading, error]);

  if (messages.length === 0 && !loading && !error) {
    return null;
  }

  return (
    <div className="chat-container card">
      <div className="chat-history">
        {messages.map((msg) => (
          <AgentMessage key={msg.id} {...msg} />
        ))}
        {loading && (
          <div className="chat-message animate-fade-in">
            <div className="chat-avatar">🤖</div>
            <div className="chat-content-wrapper">
              <div className="chat-header">
                <span className="chat-agent-name">System</span>
              </div>
              <div className="chat-bubble thinking-bubble">
                <span className="dot">.</span><span className="dot">.</span><span className="dot">.</span>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
    </div>
  );
};

export default AgentChat;
