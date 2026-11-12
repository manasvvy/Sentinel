import React, { useState, useEffect, useRef, useCallback } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function generateSessionId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

function ConfidenceBadge({ state, score }) {
  const labels = { confident: 'CONFIDENT', cautious: 'CAUTIOUS', guessing: 'GUESSING' };
  return (
    <span className={`confidence-badge confidence-${state}`}>
      <span className="badge-label">{labels[state] || state.toUpperCase()}</span>
      <span className="badge-score">{(score * 100).toFixed(0)}%</span>
    </span>
  );
}

function ReasoningPanel({ reasoning }) {
  const [open, setOpen] = useState(false);
  if (!reasoning || reasoning.length === 0) return null;
  return (
    <div className="reasoning-panel">
      <button className="reasoning-toggle" onClick={() => setOpen(o => !o)} aria-expanded={open}>
        {open ? '▾ Hide reasoning' : '▸ Show reasoning'}
      </button>
      {open && (
        <ul className="reasoning-list">
          {reasoning.map((r, i) => <li key={i}>{r}</li>)}
        </ul>
      )}
    </div>
  );
}

function CorrectionForm({ sessionId, onCorrect, onCancel }) {
  const [text, setText] = useState('');
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/correct`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, correct_info: text, note: note || undefined }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      onCorrect(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="correction-form" onSubmit={handleSubmit}>
      <div className="correction-form-header">
        <span className="correction-label">Submit correction</span>
        <button type="button" className="correction-cancel" onClick={onCancel}>✕</button>
      </div>
      <textarea
        className="correction-input"
        placeholder="Provide the correct information…"
        value={text}
        onChange={e => setText(e.target.value)}
        rows={3}
        autoFocus
        disabled={loading}
      />
      <input
        className="correction-note"
        type="text"
        placeholder="Optional note (e.g. source)"
        value={note}
        onChange={e => setNote(e.target.value)}
        disabled={loading}
      />
      {error && <div className="correction-error">Error: {error}</div>}
      <div className="correction-actions">
        <button type="submit" className="btn-primary" disabled={loading || !text.trim()}>
          {loading ? 'Sending…' : 'Submit'}
        </button>
        <button type="button" className="btn-ghost" onClick={onCancel} disabled={loading}>Cancel</button>
      </div>
    </form>
  );
}

function AiMessage({ msg, sessionId, onCorrected }) {
  const [correcting, setCorrecting] = useState(false);
  const [corrected, setCorrected] = useState(false);

  const handleCorrect = (data) => {
    setCorrected(true);
    setCorrecting(false);
    onCorrected(data);
  };

  return (
    <div className="message ai-message">
      <div className="message-meta">
        <span className="message-role">SENTINEL</span>
        <ConfidenceBadge state={msg.confidence_state} score={msg.confidence_score} />
      </div>
      <div className="message-body">{msg.response_text}</div>
      <ReasoningPanel reasoning={msg.reasoning} />
      {!correcting && !corrected && (
        <button className="correct-btn" onClick={() => setCorrecting(true)}>Correct this</button>
      )}
      {corrected && <div className="corrected-notice">✓ Correction submitted</div>}
      {correcting && (
        <CorrectionForm
          sessionId={sessionId}
          onCorrect={handleCorrect}
          onCancel={() => setCorrecting(false)}
        />
      )}
    </div>
  );
}

function SessionSummary({ summary, loading }) {
  if (loading) return <div className="session-summary loading">Loading summary…</div>;
  if (!summary) return null;

  const trendIcon = (arr) => {
    if (!arr || arr.length < 2) return '—';
    const delta = arr[arr.length - 1] - arr[0];
    if (delta > 0.05) return '↑';
    if (delta < -0.05) return '↓';
    return '→';
  };

  return (
    <div className="session-summary">
      <div className="summary-title">Session</div>
      <div className="summary-grid">
        <div className="summary-item">
          <div className="summary-value">{summary.total_messages ?? '—'}</div>
          <div className="summary-key">Messages</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">{summary.total_corrections ?? '—'}</div>
          <div className="summary-key">Corrections</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">
            {summary.correction_rate != null ? `${(summary.correction_rate * 100).toFixed(1)}%` : '—'}
          </div>
          <div className="summary-key">Correction rate</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">
            {summary.avg_confidence != null ? `${(summary.avg_confidence * 100).toFixed(0)}%` : '—'}
          </div>
          <div className="summary-key">Avg confidence</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">{trendIcon(summary.confidence_trend)}</div>
          <div className="summary-key">Trend</div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [sessionId] = useState(() => generateSessionId());
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [summary, setSummary] = useState(null);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const fetchSummary = useCallback(async () => {
    setSummaryLoading(true);
    try {
      const res = await fetch(`${API_URL}/session/${sessionId}/summary`);
      if (res.ok) setSummary(await res.json());
    } catch (_) {}
    finally { setSummaryLoading(false); }
  }, [sessionId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { id: Date.now(), role: 'user', text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: text, session_id: sessionId }),
      });
      if (!res.ok) throw new Error(`Server error: HTTP ${res.status}`);
      const data = await res.json();
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'ai', ...data }]);
      fetchSummary();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  const onCorrected = (data) => {
    fetchSummary();
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <span className="brand-icon">⬡</span>
          <span className="brand-name">Sentinel</span>
          <span className="brand-sub">AI Safety Layer</span>
        </div>
        <div className="header-session">
          <span className="session-label">Session</span>
          <code className="session-id">{sessionId.slice(0, 8)}…</code>
        </div>
      </header>

      <div className="app-body">
        <aside className="sidebar">
          <SessionSummary summary={summary} loading={summaryLoading} />
          {messages.length === 0 && (
            <div className="sidebar-hint">
              <p>Sentinel intercepts AI responses and surfaces confidence levels, reasoning, and allows corrections.</p>
              <p>Start a conversation to see it in action.</p>
            </div>
          )}
        </aside>

        <main className="chat-panel">
          <div className="messages-container">
            {messages.length === 0 && (
              <div className="empty-state">
                <div className="empty-icon">⬡</div>
                <div className="empty-title">Sentinel is ready</div>
                <div className="empty-sub">Ask anything. Confidence and reasoning will be shown for each response.</div>
              </div>
            )}

            {messages.map(msg =>
              msg.role === 'user' ? (
                <div key={msg.id} className="message user-message">
                  <div className="message-meta"><span className="message-role user-role">YOU</span></div>
                  <div className="message-body">{msg.text}</div>
                </div>
              ) : (
                <AiMessage key={msg.id} msg={msg} sessionId={sessionId} onCorrected={onCorrected} />
              )
            )}

            {loading && (
              <div className="message ai-message loading-message">
                <div className="message-meta"><span className="message-role">SENTINEL</span></div>
                <div className="typing-indicator"><span /><span /><span /></div>
              </div>
            )}

            {error && (
              <div className="error-banner">
                <strong>Error:</strong> {error}
                <button className="error-dismiss" onClick={() => setError(null)}>✕</button>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          <form className="input-form" onSubmit={sendMessage}>
            <textarea
              ref={inputRef}
              className="chat-input"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(e); } }}
              placeholder="Ask something… (Enter to send, Shift+Enter for newline)"
              rows={2}
              disabled={loading}
            />
            <button type="submit" className="send-btn" disabled={loading || !input.trim()}>
              {loading ? '…' : '→'}
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}
