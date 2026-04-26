import { X } from 'lucide-react';
import { useGraph } from '../../context/GraphContext';

const DOMAIN_LABELS = {
  water: 'Water',
  transit: 'Transit',
  health: 'Health',
  emergency: 'Emergency',
};

function CapacityBar({ value }) {
  const pct = Math.round(value * 100);
  const color =
    value >= 0.85 ? 'var(--cascade-critical)' :
    value >= 0.70 ? 'var(--cascade-high)' :
    value >= 0.50 ? 'var(--cascade-medium)' :
    'var(--cascade-low)';

  return (
    <div className="capacity-bar-wrap">
      <div className="capacity-bar-track">
        <div
          className="capacity-bar-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
      <span className="capacity-bar-label" style={{ color }}>{pct}%</span>
    </div>
  );
}

export function NodeDetail() {
  const { nodes, selectedNode, setSelectedNode } = useGraph();

  if (!selectedNode) return null;

  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));
  const connectedNodes = (selectedNode.connections || [])
    .map(id => nodeMap[id])
    .filter(Boolean);

  return (
    <div className="node-detail">
      <div className="node-detail-header">
        <div>
          <span className={`domain-badge domain-badge--${selectedNode.type}`}>
            {DOMAIN_LABELS[selectedNode.type]}
          </span>
          <span className={`status-badge status-badge--${selectedNode.status}`}>
            {selectedNode.status}
          </span>
        </div>
        <button
          className="node-detail-close"
          onClick={() => setSelectedNode(null)}
          aria-label="Close"
        >
          <X size={16} />
        </button>
      </div>

      <h3 className="node-detail-name">{selectedNode.name}</h3>
      <p className="node-detail-id">{selectedNode.id}</p>

      <div className="node-detail-section">
        <p className="node-detail-label">Current Load</p>
        <CapacityBar value={selectedNode.capacity} />
      </div>

      <div className="node-detail-section">
        <p className="node-detail-label">Centrality Score</p>
        <div className="centrality-row">
          <div className="centrality-track">
            <div
              className="centrality-bar"
              style={{
                width: `${Math.round((selectedNode.centrality_score || 0) * 100)}%`,
              }}
            />
          </div>
          <span className="centrality-value">
            {((selectedNode.centrality_score || 0) * 100).toFixed(1)}%
          </span>
        </div>
        <p className="centrality-hint">
          {(selectedNode.centrality_score || 0) > 0.6
            ? 'Critical junction — failure cascades broadly'
            : (selectedNode.centrality_score || 0) > 0.3
            ? 'Moderate impact on network'
            : 'Low cascade risk'}
        </p>
      </div>

      {connectedNodes.length > 0 && (
        <div className="node-detail-section">
          <p className="node-detail-label">
            Connected Nodes ({connectedNodes.length})
          </p>
          <ul className="connected-list">
            {connectedNodes.map(n => (
              <li key={n.id}>
                <button
                  className="connected-node-btn"
                  onClick={() => setSelectedNode(n)}
                >
                  <span className={`dot dot--${n.type}`} />
                  <span>{n.name}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
