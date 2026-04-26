import { useMemo, useCallback } from 'react';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer, LineLayer, ArcLayer } from '@deck.gl/layers';
import { Map } from 'react-map-gl/mapbox';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useGraph } from '../../context/GraphContext';
import { useCascade } from '../../context/CascadeContext';
import { useAgent } from '../../context/AgentContext';
import { useTheme } from '../../theme/ThemeProvider';
import { buildRerouteLayers } from './RerouteLayer';

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

const CASCADE_COLORS = {
  critical: [255,  51, 102],
  high:     [255, 107,  53],
  medium:   [255, 215,   0],
  low:      [0,   255, 159],
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

function cascadeColor(severity, alpha = 255) {
  if (severity >= 0.8) return [...CASCADE_COLORS.critical, alpha];
  if (severity >= 0.55) return [...CASCADE_COLORS.high,     alpha];
  if (severity >= 0.35) return [...CASCADE_COLORS.medium,   alpha];
  return [...CASCADE_COLORS.low, alpha];
}

function cssVarRgba(varName, fallback, alpha) {
  if (typeof window === 'undefined') return [...fallback, alpha];
  const value = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
  const hex = value.startsWith('#') ? value.slice(1) : '';
  if (hex.length !== 6) return [...fallback, alpha];
  return [
    parseInt(hex.slice(0, 2), 16),
    parseInt(hex.slice(2, 4), 16),
    parseInt(hex.slice(4, 6), 16),
    alpha,
  ];
}

export function CityMap() {
  const { nodes, edges, selectedNode, setSelectedNode, loading, error } = useGraph();
  const { affectedNodes, originNodeId, cascadeActive, reroute } = useCascade();
  const { cvCameras, cvDetections } = useAgent();
  const { theme } = useTheme();

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

  const cameraMarkers = useMemo(() => (
    cvCameras.map(camera => ({
      ...camera,
      kind: 'Camera feed',
      result: cvDetections[camera.id],
      anomaly: Boolean(cvDetections[camera.id]?.anomaly_detected),
    }))
  ), [cvCameras, cvDetections]);

  // Build cascade propagation path edges for overlay
  const cascadePathEdges = useMemo(() => {
    if (!cascadeActive) return [];
    const pairs = [];
    for (const [nodeId, info] of Object.entries(affectedNodes)) {
      const path = info.path ?? [];
      for (let i = 1; i < path.length; i++) {
        const src = nodeMap[path[i - 1]];
        const tgt = nodeMap[path[i]];
        if (src && tgt) {
          pairs.push({ src, tgt, severity: info.severity });
        }
      }
    }
    return pairs;
  }, [affectedNodes, cascadeActive, nodeMap]);

  const layers = useMemo(() => {
    if (!nodes.length) return [];

    const baseLayers = [
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
      // Glow ring
      new ScatterplotLayer({
        id: 'nodes-glow',
        data: nodes,
        getPosition: d => [d.lng, d.lat],
        getRadius: d => {
          if (cascadeActive && affectedNodes[d.id]) {
            return 35 + affectedNodes[d.id].severity * 40;
          }
          return 20 + (d.centrality_score ?? 0) * 30;
        },
        getFillColor: d => {
          if (cascadeActive && affectedNodes[d.id]) {
            return cascadeColor(affectedNodes[d.id].severity, 80);
          }
          return getColor(d.type, theme, Math.round(30 + (d.centrality_score ?? 0) * 50));
        },
        radiusUnits: 'pixels',
        pickable: false,
        updateTriggers: { getRadius: [affectedNodes, cascadeActive], getFillColor: [affectedNodes, cascadeActive, theme] },
      }),
      // Node fill
      new ScatterplotLayer({
        id: 'nodes',
        data: nodes,
        getPosition: d => [d.lng, d.lat],
        getRadius: d => 8 + (d.centrality_score ?? 0) * 16,
        getFillColor: d => {
          if (d.id === originNodeId) return [255, 51, 102, 255];
          if (cascadeActive && affectedNodes[d.id]) return cascadeColor(affectedNodes[d.id].severity, 230);
          if (selectedNode?.id === d.id) return [255, 255, 255, 255];
          return getColor(d.type, theme, 220);
        },
        getLineColor: d => {
          if (d.id === originNodeId) return [255, 51, 102, 255];
          return getColor(d.type, theme, 255);
        },
        lineWidthMinPixels: 1.5,
        stroked: true,
        radiusUnits: 'pixels',
        pickable: true,
        autoHighlight: true,
        highlightColor: [255, 255, 255, 80],
        updateTriggers: {
          getFillColor: [selectedNode?.id, theme, affectedNodes, originNodeId, cascadeActive],
          getLineColor:  [originNodeId],
        },
      }),
    ];

    // Cascade propagation path overlay
    if (cascadeActive && cascadePathEdges.length > 0) {
      baseLayers.push(
        new LineLayer({
          id: 'cascade-paths',
          data: cascadePathEdges,
          getSourcePosition: d => [d.src.lng, d.src.lat],
          getTargetPosition: d => [d.tgt.lng, d.tgt.lat],
          getColor: d => cascadeColor(d.severity, 200),
          getWidth: 2.5,
          widthUnits: 'pixels',
          pickable: false,
          updateTriggers: { getColor: [affectedNodes] },
        })
      );
    }

    baseLayers.push(...buildRerouteLayers({ reroute, nodeMap }));

    if (cameraMarkers.length > 0) {
      baseLayers.push(
        new ScatterplotLayer({
          id: 'cv-camera-anomaly-rings',
          data: cameraMarkers.filter(camera => camera.anomaly),
          getPosition: d => [d.lng, d.lat],
          getRadius: 34,
          getFillColor: cssVarRgba('--accent-orange', [255, 107, 53], 80),
          radiusUnits: 'pixels',
          pickable: false,
        }),
        new ScatterplotLayer({
          id: 'cv-camera-markers',
          data: cameraMarkers,
          getPosition: d => [d.lng, d.lat],
          getRadius: d => d.anomaly ? 11 : 8,
          getFillColor: d => d.anomaly
            ? cssVarRgba('--accent-orange', [255, 107, 53], 240)
            : cssVarRgba('--accent-blue', [0, 212, 255], 220),
          getLineColor: cssVarRgba('--bg-primary', [10, 14, 26], 255),
          lineWidthMinPixels: 2,
          stroked: true,
          radiusUnits: 'pixels',
          pickable: true,
          updateTriggers: {
            getRadius: [cameraMarkers],
            getFillColor: [cameraMarkers, theme],
          },
        }),
      );
    }

    return baseLayers;
  }, [nodes, intraDomainEdges, crossDomainEdges, selectedNode, theme, affectedNodes, originNodeId, cascadeActive, cascadePathEdges, reroute, nodeMap, cameraMarkers]);

  const handleClick = useCallback(
    ({ object }) => {
      if (!object) {
        setSelectedNode(null);
        return;
      }
      if (object.id && object.type) {
        setSelectedNode(object);
      }
    },
    [setSelectedNode],
  );

  const getTooltip = useCallback(({ object }) => {
    if (!object) return null;
    if (object.kind) {
      if (object.kind === 'Camera feed') {
        return {
          html: `
            <div class="map-tooltip">
              <strong>${object.name}</strong>
              <span class="tt-type">DOT camera · ${object.anomaly ? 'anomaly active' : 'monitoring'}</span>
              <span class="tt-score">Severity ${Number(object.result?.overall_severity ?? 0).toFixed(1)}</span>
            </div>`,
          style: { background: 'transparent', padding: 0, border: 'none' },
        };
      }
      return {
        html: `
          <div class="map-tooltip">
            <strong>${object.kind}</strong>
            <span class="tt-type">Added delay ${Number(object.delayMinutes ?? 0).toFixed(1)} min</span>
          </div>`,
        style: { background: 'transparent', padding: 0, border: 'none' },
      };
    }
    const score = ((object.centrality_score ?? 0) * 100).toFixed(1);
    const cascadeInfo = affectedNodes[object.id];
    return {
      html: `
        <div class="map-tooltip">
          <strong>${object.name}</strong>
          <span class="tt-type">${object.type} · ${object.status}</span>
          <span class="tt-score">Centrality ${score}% · Load ${Math.round(object.capacity * 100)}%</span>
          ${cascadeInfo ? `<span class="tt-cascade">Cascade impact in ${cascadeInfo.minutes?.toFixed(1)}m · Severity ${(cascadeInfo.severity * 10).toFixed(1)}</span>` : ''}
        </div>`,
      style: { background: 'transparent', padding: 0, border: 'none' },
    };
  }, [affectedNodes]);

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
