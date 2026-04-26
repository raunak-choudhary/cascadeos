import { useCascade } from '../../context/CascadeContext';

const DOMAIN_COLORS = {
  water:     'var(--agent-water)',
  transit:   'var(--agent-transit)',
  health:    'var(--agent-health)',
  emergency: 'var(--agent-emergency)',
};

function severityLabel(s) {
  if (s >= 0.8) return 'CRITICAL';
  if (s >= 0.55) return 'HIGH';
  if (s >= 0.35) return 'MEDIUM';
  return 'LOW';
}

function severityClass(s) {
  if (s >= 0.8) return 'cascade-critical';
  if (s >= 0.55) return 'cascade-high';
  if (s >= 0.35) return 'cascade-medium';
  return 'cascade-low';
}

export function CascadeTimeline() {
  const { cascadeEvents, cascadeActive, isComplete, originNodeId } = useCascade();

  if (!cascadeActive && cascadeEvents.length === 0) return null;

  return (
    <div className="cascade-timeline">
      <div className="cascade-timeline-header">
        <span className="cascade-timeline-title">Cascade Timeline</span>
        {!isComplete && cascadeActive && (
          <span className="cascade-timeline-live">
            <span className="live-dot" /> LIVE
          </span>
        )}
        {isComplete && (
          <span className="cascade-timeline-complete">
            {cascadeEvents.length} nodes affected
          </span>
        )}
      </div>

      <div className="cascade-timeline-scroll">
        {cascadeEvents.map((ev, i) => (
          <div
            key={`${ev.node_id}-${i}`}
            className={`ct-item ct-item--${severityClass(ev.severity)} ${i === 0 ? 'ct-item--origin' : ''}`}
            style={{ '--domain-color': DOMAIN_COLORS[ev.domain] ?? 'var(--border)' }}
          >
            <div className="ct-time">
              {ev.predicted_impact_minutes === 0
                ? 'NOW'
                : `+${ev.predicted_impact_minutes.toFixed(1)}m`}
            </div>
            <div className="ct-connector">
              <div className="ct-dot" />
              {i < cascadeEvents.length - 1 && <div className="ct-line" />}
            </div>
            <div className="ct-body">
              <span className="ct-name">{ev.node_name}</span>
              <div className="ct-meta">
                <span
                  className="ct-domain-badge"
                  style={{ color: DOMAIN_COLORS[ev.domain] }}
                >
                  {ev.domain}
                </span>
                <span className={`ct-severity severity--${severityClass(ev.severity)}`}>
                  {severityLabel(ev.severity)}
                </span>
                <span className="ct-depth">depth {ev.cascade_depth}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
