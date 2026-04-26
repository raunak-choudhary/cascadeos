import { useAgent } from '../../context/AgentContext';

const DOMAIN_COLORS = {
  water:     'var(--agent-water)',
  transit:   'var(--agent-transit)',
  health:    'var(--agent-health)',
  emergency: 'var(--agent-emergency)',
};

function severityClass(score) {
  if (score >= 8) return 'cascade-critical';
  if (score >= 6) return 'cascade-high';
  if (score >= 4) return 'cascade-medium';
  return 'cascade-low';
}

export function AlertFeed() {
  const { alerts, surges } = useAgent();

  return (
    <div className="alert-feed-wrap">
      <div className="panel-header">
        <h2 className="panel-title">Alert Feed</h2>
        <p className="panel-subtitle">Live severity-ranked alerts from all agent domains</p>
      </div>

      {alerts.length === 0 ? (
        <div className="alert-empty">
          <span className="alert-empty-icon">✅</span>
          <p>No active alerts. All systems nominal.</p>
        </div>
      ) : (
        <div className="alert-list">
          {alerts.map((alert, i) => (
            <div key={alert.id ?? i} className="alert-item alert-item--slide-in">
              <div className="alert-item-header">
                <span
                  className="alert-domain-badge"
                  style={{ background: DOMAIN_COLORS[alert.domain] ?? 'var(--border)' }}
                >
                  {alert.domain}
                </span>
                <span className={`alert-severity severity--${severityClass(alert.severity)}`}>
                  {alert.severity?.toFixed(1)}
                </span>
                <span className="alert-time">
                  {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString() : ''}
                </span>
              </div>
              <p className="alert-signal">{alert.signal}</p>
              {alert.reasoning && (
                <p className="alert-reasoning">{alert.reasoning}</p>
              )}
              {alert.affected_nodes?.length > 0 && (
                <div className="alert-nodes">
                  {alert.affected_nodes.map(n => (
                    <span key={n} className="alert-node-tag">{n}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {surges.length > 0 && (
        <div className="surges-section">
          <h3 className="surges-title">311 Surge Detections</h3>
          {surges.slice(0, 5).map((surge, i) => (
            <div key={i} className="surge-item">
              <span className="surge-nta">{surge.nta_code}</span>
              <span className="surge-type">{surge.dominant_complaint_type}</span>
              <span className="surge-count">{surge.complaint_count} reports</span>
              <span className={`alert-severity severity--${severityClass(surge.severity_score)}`}>
                {surge.severity_score?.toFixed(1)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
