import { useMemo, useCallback, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useGraph } from '../../context/GraphContext';

// ── Geographic → canvas projection ──────────────────────────────────────────
const LAT_MIN = 40.48, LAT_MAX = 40.91;
const LNG_MIN = -74.26, LNG_MAX = -73.68;
const W = 2400,         H = 1400;

function geoToCanvas(lat, lng) {
  const x = ((lng - LNG_MIN) / (LNG_MAX - LNG_MIN)) * W;
  const y = H - ((lat - LAT_MIN) / (LAT_MAX - LAT_MIN)) * H;
  return { x, y };
}

// ── Domain colours ───────────────────────────────────────────────────────────
const DOMAIN_COLOR = {
  water:     { bg: 'rgba(0,212,255,0.12)',  border: '#00d4ff' },
  transit:   { bg: 'rgba(255,107,53,0.12)', border: '#ff6b35' },
  health:    { bg: 'rgba(255,51,102,0.12)', border: '#ff3366' },
  emergency: { bg: 'rgba(0,255,159,0.12)',  border: '#00ff9f' },
};

const EDGE_COLOR = {
  dependency:  '#ff3366',
  operational: '#00d4ff',
  proximity:   '#4a7090',
};

function buildRFNodes(nodes) {
  return nodes.map(node => {
    const pos = geoToCanvas(node.lat, node.lng);
    const c   = DOMAIN_COLOR[node.type] ?? DOMAIN_COLOR.water;
    const cs  = node.centrality_score ?? 0;

    return {
      id:       node.id,
      position: pos,
      data:     { label: node.name, node },
      style: {
        background:  c.bg,
        border:      `${Math.round(1 + cs * 1.5)}px solid ${c.border}`,
        borderRadius: 8,
        padding:     '3px 7px',
        fontSize:    `${Math.round(9 + cs * 4)}px`,
        color:       'var(--text-primary)',
        maxWidth:    130,
        minWidth:    80,
        boxShadow:   cs > 0.5
          ? `0 0 ${Math.round(cs * 18)}px ${c.border}44`
          : 'none',
        cursor: 'pointer',
      },
    };
  });
}

function buildRFEdges(edges) {
  return edges.map((e, i) => ({
    id:     `rf-e-${i}`,
    source: e.source,
    target: e.target,
    style: {
      stroke:          EDGE_COLOR[e.type] ?? '#4a7090',
      strokeWidth:     Math.max(0.5, e.weight * 1.5),
      strokeDasharray: e.type === 'dependency' ? '6 4' : undefined,
      opacity:         0.55,
    },
    markerEnd: {
      type:  'arrowclosed',
      color: EDGE_COLOR[e.type] ?? '#4a7090',
    },
  }));
}

export function SystemGraph() {
  const { nodes: rawNodes, edges: rawEdges, setSelectedNode, loading, error } = useGraph();

  const [rfNodes, setRfNodes, onNodesChange] = useNodesState([]);
  const [rfEdges, setRfEdges, onEdgesChange] = useEdgesState([]);

  // Sync React Flow state whenever API data arrives
  useEffect(() => {
    if (rawNodes.length) setRfNodes(buildRFNodes(rawNodes));
  }, [rawNodes, setRfNodes]);

  useEffect(() => {
    if (rawEdges.length) setRfEdges(buildRFEdges(rawEdges));
  }, [rawEdges, setRfEdges]);

  const onNodeClick = useCallback(
    (_, rfNode) => setSelectedNode(rfNode.data.node),
    [setSelectedNode],
  );

  if (loading) {
    return (
      <div className="map-placeholder">
        <div className="map-loading">
          <div className="spinner" />
          <p>Building system graph…</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="map-placeholder">
        <p className="map-error">Failed to load graph: {error}</p>
      </div>
    );
  }

  return (
    <div className="system-graph-wrap">
      <ReactFlow
        nodes={rfNodes}
        edges={rfEdges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        fitView
        fitViewOptions={{ padding: 0.08 }}
        minZoom={0.05}
        maxZoom={4}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="var(--border-subtle)" gap={28} />
        <Controls
          style={{
            background:   'var(--bg-card)',
            border:       '1px solid var(--border)',
            borderRadius: 8,
          }}
        />
        <MiniMap
          nodeColor={n => DOMAIN_COLOR[n.data?.node?.type]?.border ?? '#4a7090'}
          maskColor="rgba(0,0,0,0.4)"
          style={{
            background:   'var(--bg-card)',
            border:       '1px solid var(--border)',
            borderRadius: 8,
          }}
        />
      </ReactFlow>

      {/* Legend */}
      <div className="graph-legend">
        <div className="graph-legend-section">
          <p className="legend-title">Domains</p>
          {Object.entries(DOMAIN_COLOR).map(([type, c]) => (
            <div key={type} className="legend-item">
              <span className="legend-swatch" style={{ background: c.border }} />
              <span>{type.charAt(0).toUpperCase() + type.slice(1)}</span>
            </div>
          ))}
        </div>
        <div className="graph-legend-section">
          <p className="legend-title">Edge Types</p>
          {Object.entries(EDGE_COLOR).map(([type, color]) => (
            <div key={type} className="legend-item">
              <span
                className="legend-swatch"
                style={{ background: color, width: 18, height: 2, borderRadius: 1 }}
              />
              <span>{type}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
