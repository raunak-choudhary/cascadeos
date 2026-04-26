import { createContext, useContext, useState, useCallback } from 'react';

const CascadeContext = createContext(null);

export function useCascade() {
  return useContext(CascadeContext);
}

export function CascadeProvider({ children }) {
  const [cascadeActive, setCascadeActive] = useState(false);
  const [originNodeId, setOriginNodeId] = useState(null);
  const [cascadeEvents, setCascadeEvents] = useState([]); // ordered list of arrived events
  const [affectedNodes, setAffectedNodes] = useState({}); // nodeId → { severity, status, depth }
  const [isComplete, setIsComplete] = useState(false);

  const handleWsMessage = useCallback((msg) => {
    switch (msg.type) {
      case 'cascade_start':
        setCascadeActive(true);
        setIsComplete(false);
        setOriginNodeId(msg.payload.origin_node_id);
        setCascadeEvents([]);
        setAffectedNodes({});
        break;

      case 'cascade_node':
        setCascadeEvents(prev => [...prev, msg.payload]);
        setAffectedNodes(prev => ({
          ...prev,
          [msg.payload.node_id]: {
            severity: msg.payload.severity,
            status: msg.payload.status,
            depth: msg.payload.cascade_depth,
            path: msg.payload.propagation_path,
            minutes: msg.payload.predicted_impact_minutes,
          },
        }));
        break;

      case 'cascade_complete':
        setIsComplete(true);
        break;

      case 'simulation_reset':
        setCascadeActive(false);
        setOriginNodeId(null);
        setCascadeEvents([]);
        setAffectedNodes({});
        setIsComplete(false);
        break;

      default:
        break;
    }
  }, []);

  return (
    <CascadeContext.Provider value={{
      cascadeActive,
      originNodeId,
      cascadeEvents,
      affectedNodes,
      isComplete,
      handleWsMessage,
    }}>
      {children}
    </CascadeContext.Provider>
  );
}
