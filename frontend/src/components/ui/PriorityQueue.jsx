import { useAgent } from '../../context/AgentContext';

const DOMAIN_COLORS = {
  water:     'var(--agent-water)',
  transit:   'var(--agent-transit)',
  health:    'var(--agent-health)',
  emergency: 'var(--agent-emergency)',
};

export function PriorityQueueViz() {
  const { queueSnapshot } = useAgent();

  return (
    <div className="pq-viz">
      <div className="pq-header">
        <h3 className="pq-title">Max Heap Alert Queue</h3>
        <span className="pq-count">{queueSnapshot.length} items</span>
      </div>
      <p className="pq-subtitle">Built with Python heapq — highest severity processed first</p>

      {queueSnapshot.length === 0 ? (
        <p className="pq-empty">Queue empty — no pending alerts</p>
      ) : (
        <div className="pq-rows">
          {queueSnapshot.map((item, i) => (
            <div key={item.id ?? i} className="pq-row">
              <span className="pq-rank">#{i + 1}</span>
              <span
                className="pq-domain"
                style={{ color: DOMAIN_COLORS[item.domain] ?? 'var(--text-secondary)' }}
              >
                {item.domain}
              </span>
              <div className="pq-bar-wrap">
                <div
                  className="pq-bar"
                  style={{
                    width: `${(item.severity / 10) * 100}%`,
                    background: DOMAIN_COLORS[item.domain] ?? 'var(--border)',
                  }}
                />
              </div>
              <span className="pq-score">{item.severity?.toFixed(1)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
