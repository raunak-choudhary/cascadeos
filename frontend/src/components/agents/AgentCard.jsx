import { useEffect, useRef } from 'react';

const DOMAIN_META = {
  water:     { label: 'Water Systems',   icon: '💧', cssVar: '--agent-water' },
  transit:   { label: 'Transit Network', icon: '🚇', cssVar: '--agent-transit' },
  health:    { label: 'Health Systems',  icon: '🏥', cssVar: '--agent-health' },
  emergency: { label: 'Emergency Svcs',  icon: '🚨', cssVar: '--agent-emergency' },
};

function TypewriterText({ text }) {
  const spanRef = useRef(null);
  const prevText = useRef('');

  useEffect(() => {
    if (!text || text === prevText.current) return;
    prevText.current = text;

    const el = spanRef.current;
    if (!el) return;

    el.style.animation = 'none';
    el.textContent = '';
    // Trigger reflow
    void el.offsetWidth;
    el.style.animation = '';
    el.setAttribute('data-text', text);
  }, [text]);

  return (
    <span
      ref={spanRef}
      className="agent-typewriter"
      data-text={text ?? ''}
    />
  );
}

export function AgentCard({ agent }) {
  const meta = DOMAIN_META[agent.domain] ?? { label: agent.domain, icon: '⚡', cssVar: '--text-primary' };
  const isAlert = agent.status === 'alert';
  const isAnalyzing = agent.status === 'analyzing';

  const confidence = agent.confidence != null
    ? `${Math.round(agent.confidence * 100)}%`
    : '—';

  const updatedAt = agent.last_updated
    ? new Date(agent.last_updated).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : 'waiting…';

  return (
    <div
      className={`agent-card ${isAlert ? 'agent-card--alert' : ''}`}
      style={{ '--domain-color': `var(${meta.cssVar})` }}
    >
      <div className="agent-card-header">
        <span className="agent-icon">{meta.icon}</span>
        <span className="agent-label">{meta.label}</span>
        <span className={`agent-status-dot agent-status-dot--${agent.status}`} />
        <span className="agent-status-text">{agent.status}</span>
      </div>

      {agent.last_signal && (
        <div className="agent-signal">
          <TypewriterText text={agent.last_signal} />
        </div>
      )}

      {agent.last_reasoning && (
        <p className="agent-reasoning">{agent.last_reasoning}</p>
      )}

      <div className="agent-footer">
        <span className="agent-confidence">
          Confidence <strong>{confidence}</strong>
        </span>
        <span className="agent-updated">{updatedAt}</span>
      </div>
    </div>
  );
}
