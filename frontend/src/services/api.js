const BASE_URL = import.meta.env.VITE_API_URL;

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const api = {
  health: () => request('/health'),
  getNodes: () => request('/graph/nodes'),
  getEdges: () => request('/graph/edges'),
  triggerSimulation: (body) =>
    request('/simulation/trigger', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),
  resetSimulation: () =>
    request('/simulation/reset', { method: 'POST' }),
  getScenarios: () => request('/simulation/scenarios'),
  generateBriefing: () =>
    request('/briefing/generate', { method: 'POST' }),
};
