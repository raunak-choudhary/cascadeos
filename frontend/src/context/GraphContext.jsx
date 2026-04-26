import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { api } from '../services/api';

const GraphContext = createContext(null);

export function GraphProvider({ children }) {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const reloadGraph = useCallback(() => {
    setLoading(true);
    setError(null);
    Promise.all([api.getNodes(), api.getEdges()])
      .then(([n, e]) => {
        setNodes(n);
        setEdges(e);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    reloadGraph();
  }, [reloadGraph]);

  return (
    <GraphContext.Provider
      value={{ nodes, edges, selectedNode, setSelectedNode, loading, error, reloadGraph }}
    >
      {children}
    </GraphContext.Provider>
  );
}

export function useGraph() {
  const ctx = useContext(GraphContext);
  if (!ctx) throw new Error('useGraph must be used inside GraphProvider');
  return ctx;
}
