import { useMemo, useCallback } from 'react';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer, LineLayer, ArcLayer } from '@deck.gl/layers';
import { Map } from 'react-map-gl/mapbox';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useGraph } from '../../context/GraphContext';
import { useTheme } from '../../theme/ThemeProvider';

// ── Color palette matching CSS custom properties ─────────────────────────────
const DOMAIN_COLORS = {
  dark: {
    water:     [0,   212, 255],
    transit:   [255, 107,  53],
    health:    [255,  51, 102],
    emergency: [0,   255, 159],
  },
  light: {
    water:     [0,   102, 204],
    transit:   [217,  79,  30],
    health:    [204,   0,  51],
    emergency: [0,   128,  63],
  },
};

const MAP_STYLES = {
  dark:  'mapbox://styles/mapbox/dark-v11',
  light: 'mapbox://styles/mapbox/light-v11',
};

const INITIAL_VIEW = {
  longitude: -73.9857,
  latitude:   40.7484,
  zoom:       11,
  pitch:      20,
  bearing:    0,
};

function getColor(type, theme, alpha = 255) {
  const palette = DOMAIN_COLORS[theme] ?? DOMAIN_COLORS.dark;
  const rgb = palette[type] ?? [150, 150, 150];
  return [...rgb, alpha];
}

export function CityMap() {
  const { nodes, edges, selectedNode, setSelectedNode, loading, error } = useGraph();
  const { theme } = useTheme();

  // Build a lookup so layers can resolve positions from edge source/target IDs
  const nodeMap = useMemo(
    () => Object.fromEntries(nodes.map(n => [n.id, n])),
    [nodes],
  );

  const { intraDomainEdges, crossDomainEdges } = useMemo(() => {
    const intra = [];
    const cross = [];
    for (const e of edges) {
      const src = nodeMap[e.source];
      const tgt = nodeMap[e.target];
      if (!src || !tgt) continue;
      const enriched = { ...e, src, tgt };
      if (src.type === tgt.type) intra.push(enriched);
      else cross.push(enriched);
    }
    return { intraDomainEdges: intra, crossDomainEdges: cross };
  }, [edges, nodeMap]);

  const layers = useMemo(() => {
    if (!nodes.length) return [];

    return [
      // Intra-domain edges — flat lines
      new LineLayer({
        id: 'edges-intra',
        data: intraDomainEdges,
        getSourcePosition: d => [d.src.lng, d.src.lat],
        getTargetPosition: d => [d.tgt.lng, d.tgt.lat],
        getColor: d => getColor(d.src.type, theme, 60),
        getWidth: d => Math.max(1, d.weight * 2),
        widthUnits: 'pixels',
        pickable: false,
      }),

      // Cross-domain edges — arcs showing dependencies
      new ArcLayer({
        id: 'edges-cross',
        data: crossDomainEdges,
        getSourcePosition: d => [d.src.lng, d.src.lat],
        getTargetPosition: d => [d.tgt.lng, d.tgt.lat],
        getSourceColor: d => getColor(d.src.type, theme, 120),
        getTargetColor: d => getColor(d.tgt.type, theme, 120),
        getWidth: d => Math.max(1, d.weight * 2.5),
        widthUnits: 'pixels',
        greatCircle: false,
        pickable: false,
      }),

      // Node glow ring (outer, low alpha)
      new ScatterplotLayer({
        id: 'nodes-glow',
        data: nodes,
        getPosition: d => [d.lng, d.lat],
        getRadius: d => 20 + (d.centrality_score ?? 0) * 30,
        getFillColor: d => getColor(d.type, theme, Math.round(30 + (d.centrality_score ?? 0) * 50)),
        radiusUnits: 'pixels',
        pickable: false,
      }),

      // Node fill (main circle)
      new ScatterplotLayer({
        id: 'nodes',
        data: nodes,
        getPosition: d => [d.lng, d.lat],
        getRadius: d => 8 + (d.centrality_score ?? 0) * 16,
        getFillColor: d =>
          selectedNode?.id === d.id
            ? [255, 255, 255, 255]
            : getColor(d.type, theme, 220),
        getLineColor: d => getColor(d.type, theme, 255),
        lineWidthMinPixels: 1.5,
        stroked: true,
        radiusUnits: 'pixels',
        pickable: true,
        autoHighlight: true,
        highlightColor: [255, 255, 255, 80],
        updateTriggers: {
          getFillColor: [selectedNode?.id, theme],
        },
      }),
    ];
  }, [nodes, intraDomainEdges, crossDomainEdges, selectedNode, theme]);

  const handleClick = useCallback(
    ({ object }) => {
      setSelectedNode(object ?? null);
    },
    [setSelectedNode],
  );

  const getTooltip = useCallback(
    ({ object }) => {
      if (!object) return null;
      const score = ((object.centrality_score ?? 0) * 100).toFixed(1);
      return {
        html: `
          <div class="map-tooltip">
            <strong>${object.name}</strong>
            <span class="tt-type">${object.type} · ${object.status}</span>
            <span class="tt-score">Centrality ${score}% · Load ${Math.round(object.capacity * 100)}%</span>
          </div>`,
        style: {
          background: 'transparent',
          padding: 0,
          border: 'none',
        },
      };
    },
    [],
  );

  if (loading) {
    return (
      <div className="map-placeholder">
        <div className="map-loading">
          <div className="spinner" />
          <p>Loading infrastructure graph…</p>
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
    <div className="city-map-wrap">
      <DeckGL
        initialViewState={INITIAL_VIEW}
        controller={{ dragRotate: true }}
        layers={layers}
        onClick={handleClick}
        getTooltip={getTooltip}
      >
        <Map
          mapboxAccessToken={import.meta.env.VITE_MAPBOX_TOKEN}
          mapStyle={MAP_STYLES[theme]}
          reuseMaps
        />
      </DeckGL>

      {/* Map legend */}
      <div className="map-legend">
        {['water', 'transit', 'health', 'emergency'].map(type => (
          <div key={type} className="legend-item">
            <span className={`legend-dot legend-dot--${type}`} />
            <span>{type.charAt(0).toUpperCase() + type.slice(1)}</span>
          </div>
        ))}
      </div>

    </div>
  );
}
