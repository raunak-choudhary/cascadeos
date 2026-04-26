import { createContext, useContext, useState, useCallback } from 'react';

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

      default:
        break;
    }
  }, []);

  return (
    <AgentContext.Provider value={{ agents, alerts, queueSnapshot, surges, handleWsMessage }}>
      {children}
    </AgentContext.Provider>
  );
}
