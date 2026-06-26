import { useEffect, useRef, useState } from 'react';
import { sendChatMessage } from '../api';

const quickPrompts = [
  'Explain decision',
  'Why manual review?',
  'What should the analyst do?',
  'Summarize for manager',
  'Show monitoring risks',
  'Explain LangSmith trace',
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

const AgentChat = ({ incident, analysisResult }) => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Analysis context loaded. Ask about the decision, monitoring signals, LangSmith trace, or recommended analyst actions.',
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
    if (!trimmed || sending) return;

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
        analysisResult,
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
    <section className="card chat-panel">
      <div className="section-header">
        <div>
          <h2>Agent Chat</h2>
          <p className="text-muted">Real chat connected to the current incident analysis context.</p>
        </div>
        {error && <span className="badge badge-warning">chat unavailable</span>}
      </div>

      <div className="quick-actions">
        {quickPrompts.map((prompt) => (
          <button className="btn btn-secondary" type="button" key={prompt} onClick={() => submitMessage(prompt)} disabled={sending}>
            {prompt}
          </button>
        ))}
      </div>

      <div className="chat-history">
        {messages.map((message) => (
          <div className={`chat-message ${message.role === 'user' ? 'chat-message-user' : ''}`} key={message.id}>
            <div className="chat-avatar">{message.role === 'user' ? '👤' : '🤖'}</div>
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
            <div className="chat-avatar">🤖</div>
            <div className="chat-content-wrapper">
              <div className="chat-header">
                <span className="chat-agent-name">Finance Agent</span>
              </div>
              <div className="chat-bubble thinking-bubble">
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
          disabled={sending}
        />
        <button className="btn btn-primary btn-inline" type="submit" disabled={sending || !input.trim()}>
          Send
        </button>
      </form>
    </section>
  );
};

export default AgentChat;
