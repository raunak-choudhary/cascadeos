import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { api } from '../services/api';

const AgentContext = createContext(null);

export function useAgent() {
  return useContext(AgentContext);
}

const DOMAIN_ORDER = ['water', 'transit', 'health', 'emergency'];

function makeInitialState() {
  return Object.fromEntries(
    DOMAIN_ORDER.map(d => [d, {
      domain: d,
      status: 'idle',
      last_signal: null,
      last_reasoning: null,
      confidence: null,
      last_updated: null,
    }])
  );
}

export function AgentProvider({ children }) {
  const [agents, setAgents] = useState(makeInitialState);
  const [alerts, setAlerts] = useState([]);
  const [queueSnapshot, setQueueSnapshot] = useState([]);
  const [surges, setSurges] = useState([]);
  const [cvCameras, setCvCameras] = useState([]);
  const [cvDetections, setCvDetections] = useState({});
  const [cvStatus, setCvStatus] = useState({ status: 'idle', message: null });

  useEffect(() => {
    let cancelled = false;
    api.getCameras()
      .then(cameras => {
        if (!cancelled) setCvCameras(cameras);
      })
      .catch(err => {
        if (!cancelled) setCvStatus({ status: 'error', message: err.message });
      });
    return () => { cancelled = true; };
  }, []);

  const handleWsMessage = useCallback((msg) => {
    switch (msg.type) {
      case 'agent_update':
        setAgents(prev => ({
          ...prev,
          [msg.payload.domain]: { ...prev[msg.payload.domain], ...msg.payload },
        }));
        break;

      case 'alert':
        setAlerts(prev => {
          const next = [msg.payload, ...prev].slice(0, 50); // keep last 50
          return next.sort((a, b) => b.severity - a.severity);
        });
        break;

      case 'queue_snapshot':
        setQueueSnapshot(msg.payload);
        break;

      case '311_surge':
        setSurges(prev => {
          const next = [msg.payload, ...prev].slice(0, 20);
          return next;
        });
        break;

      case 'cv_update':
        setCvDetections(prev => ({
          ...prev,
          [msg.payload.camera_id]: msg.payload,
        }));
        setCvCameras(prev => {
          if (prev.some(camera => camera.id === msg.payload.camera_id)) return prev;
          return [
            ...prev,
            {
              id: msg.payload.camera_id,
              name: msg.payload.camera_name,
              lat: msg.payload.lat,
              lng: msg.payload.lng,
            },
          ];
        });
        setCvStatus({ status: 'live', message: null });
        break;

      case 'cv_status':
        setCvStatus(msg.payload);
        break;

      default:
        break;
    }
  }, []);

  return (
    <AgentContext.Provider value={{
      agents,
      alerts,
      queueSnapshot,
      surges,
      cvCameras,
      cvDetections,
      cvStatus,
      handleWsMessage,
    }}>
      {children}
    </AgentContext.Provider>
  );
}
