import { useState, useCallback } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { AppShell } from './components/layout/AppShell';
import { AgentProvider, useAgent } from './context/AgentContext';
import { CascadeProvider, useCascade } from './context/CascadeContext';
import { useWebSocket } from './hooks/useWebSocket';

function CascadeApp() {
  const [lastHeartbeat, setLastHeartbeat] = useState(null);
  const { handleWsMessage: agentHandler } = useAgent();
  const { handleWsMessage: cascadeHandler } = useCascade();

  const handleMessage = useCallback((msg) => {
    if (msg.type === 'heartbeat') {
      setLastHeartbeat(msg.timestamp);
    }
    agentHandler(msg);
    cascadeHandler(msg);
  }, [agentHandler, cascadeHandler]);

  const wsStatus = useWebSocket(handleMessage);

  return (
    <AppShell wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AgentProvider>
        <CascadeProvider>
          <CascadeApp />
        </CascadeProvider>
      </AgentProvider>
    </ThemeProvider>
  );
}
