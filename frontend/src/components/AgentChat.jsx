import { useEffect, useRef, useState } from 'react';
import { Bot, Send, UserRound, WandSparkles } from 'lucide-react';
import { sendChatMessage } from '../api';

const quickPrompts = [
  'Explain Risk',
  'Explain Fraud',
  'Explain Compliance',
  'Explain Decision',
  'Summarize Incident',
  'Generate Executive Summary',
  'Explain Monitoring',
  'Explain LangGraph Workflow',
];

const getAssistantText = (response) => (
  response?.message || response?.response || response?.answer || response?.content || JSON.stringify(response, null, 2)
);

const isBlocked = (response) => (
  response?.blocked === true ||
  response?.safety?.blocked === true ||
  response?.safety?.action === 'block' ||
  response?.safety?.final_decision?.action === 'block'
);

const AgentChat = ({ incident, analysisResult, standalone = false }) => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Analysis context loaded. Ask about risk, fraud, compliance, monitoring, LangGraph workflow or the final decision.',
    },
  ]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const submitMessage = async (text) => {
    const trimmed = text.trim();
    if (!trimmed || sending || !analysisResult) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: trimmed,
    };
    const nextMessages = [...messages, userMessage];

    setMessages(nextMessages);
    setInput('');
    setSending(true);
    setError(null);

    try {
      const response = await sendChatMessage({
        message: trimmed,
        incident,
        analysis_result: analysisResult,
        history: nextMessages.map(({ role, content }) => ({ role, content })),
      });

      setMessages((current) => [
        ...current,
        {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          content: getAssistantText(response),
          blocked: isBlocked(response),
        },
      ]);
    } catch (err) {
      const message = err.message || 'Chat request failed.';
      setError(message);
      setMessages((current) => [
        ...current,
        {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: message,
          blocked: true,
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    submitMessage(input);
  };

  return (
    <section className={`chat-panel ${standalone ? 'chat-panel-standalone' : 'panel'}`}>
      <div className="section-header">
        <div>
          <h3>Finance AI Assistant</h3>
          <p>Context-aware chat connected to the current incident, analysis result and conversation history.</p>
        </div>
        {error && <span className="badge badge-warning">chat unavailable</span>}
      </div>

      {!analysisResult && (
        <div className="notice notice-warning">
          Run an incident analysis first to give the assistant finance context.
        </div>
      )}

      <div className="quick-actions">
        {quickPrompts.map((prompt) => (
          <button className="btn btn-secondary" type="button" key={prompt} onClick={() => submitMessage(prompt)} disabled={sending || !analysisResult}>
            <WandSparkles size={15} />
            {prompt}
          </button>
        ))}
      </div>

      <div className="chat-history">
        {messages.map((message) => (
          <div className={`chat-message ${message.role === 'user' ? 'chat-message-user' : ''}`} key={message.id}>
            <div className="chat-avatar">
              {message.role === 'user' ? <UserRound size={17} /> : <Bot size={17} />}
            </div>
            <div className="chat-content-wrapper">
              <div className="chat-header">
                <span className="chat-agent-name">{message.role === 'user' ? 'You' : 'Finance Agent'}</span>
                {message.blocked && <span className="badge badge-danger">blocked by safety</span>}
              </div>
              <div className="chat-bubble">
                <p className="chat-main-content">{message.content}</p>
              </div>
            </div>
          </div>
        ))}
        {sending && (
          <div className="chat-message">
            <div className="chat-avatar"><Bot size={17} /></div>
            <div className="chat-content-wrapper">
              <div className="chat-header">
                <span className="chat-agent-name">Finance Agent</span>
              </div>
              <div className="chat-bubble thinking-bubble">
                <span>Thinking</span>
                <span className="dot">.</span><span className="dot">.</span><span className="dot">.</span>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          className="form-control"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask the agent about this incident..."
          disabled={sending || !analysisResult}
        />
        <button className="btn btn-primary btn-inline" type="submit" disabled={sending || !input.trim() || !analysisResult}>
          <Send size={17} />
          Send
        </button>
      </form>
    </section>
  );
};

export default AgentChat;
