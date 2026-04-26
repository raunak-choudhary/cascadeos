import { LineLayer } from '@deck.gl/layers';

function hexToRgba(hex, alpha) {
  const normalized = hex.trim().replace('#', '');
  if (normalized.length !== 6) return [150, 150, 150, alpha];
  return [
    parseInt(normalized.slice(0, 2), 16),
    parseInt(normalized.slice(2, 4), 16),
    parseInt(normalized.slice(4, 6), 16),
    alpha,
  ];
}

function cssColor(varName, alpha, fallback) {
  if (typeof window === 'undefined') return hexToRgba(fallback, alpha);
  const value = getComputedStyle(document.documentElement).getPropertyValue(varName);
  return hexToRgba(value || fallback, alpha);
}

function pairsForPath(path = [], nodeMap, kind, delayMinutes) {
  const pairs = [];
  for (let i = 1; i < path.length; i++) {
    const src = nodeMap[path[i - 1]];
    const tgt = nodeMap[path[i]];
    if (src && tgt) {
      pairs.push({ src, tgt, kind, delayMinutes });
    }
  }
  return pairs;
}

function interpolate(source, target, ratio) {
  return {
    lng: source.lng + (target.lng - source.lng) * ratio,
    lat: source.lat + (target.lat - source.lat) * ratio,
  };
}

function dashPairs(edges) {
  const dashed = [];
  for (const edge of edges) {
    const count = 8;
    for (let i = 0; i < count; i++) {
      const start = i / count;
      const end = start + 0.55 / count;
      dashed.push({
        ...edge,
        src: interpolate(edge.src, edge.tgt, start),
        tgt: interpolate(edge.src, edge.tgt, end),
      });
    }
  }
  return dashed;
}

export function buildRerouteLayers({ reroute, nodeMap }) {
  if (!reroute || reroute.error || !reroute.original_path || !reroute.rerouted_path) {
    return [];
  }

  const blockedEdges = pairsForPath(
    reroute.original_path,
    nodeMap,
    'Blocked corridor',
    reroute.delay_minutes,
  );
  const rerouteEdges = pairsForPath(
    reroute.rerouted_path,
    nodeMap,
    'Emergency reroute',
    reroute.delay_minutes,
  );
  const blockedColor = cssColor('--cascade-critical', 220, '#ff3366');
  const rerouteColor = cssColor('--accent-green', 230, '#00ff9f');

  return [
    new LineLayer({
      id: 'reroute-blocked',
      data: dashPairs(blockedEdges),
      getSourcePosition: d => [d.src.lng, d.src.lat],
      getTargetPosition: d => [d.tgt.lng, d.tgt.lat],
      getColor: blockedColor,
      getWidth: 4,
      widthUnits: 'pixels',
      pickable: true,
    }),
    new LineLayer({
      id: 'reroute-path',
      data: rerouteEdges,
      getSourcePosition: d => [d.src.lng, d.src.lat],
      getTargetPosition: d => [d.tgt.lng, d.tgt.lat],
      getColor: rerouteColor,
      getWidth: 4,
      widthUnits: 'pixels',
      pickable: true,
    }),
  ];
}
