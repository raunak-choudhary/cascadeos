import { useState, useCallback } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { AppShell } from './components/layout/AppShell';
import { AgentProvider, useAgent } from './context/AgentContext';
import { useWebSocket } from './hooks/useWebSocket';

function CascadeApp() {
  const [lastHeartbeat, setLastHeartbeat] = useState(null);
  const { handleWsMessage } = useAgent();

  const handleMessage = useCallback((msg) => {
    if (msg.type === 'heartbeat') {
      setLastHeartbeat(msg.timestamp);
    }
    // Route all WS messages into AgentContext
    handleWsMessage(msg);
  }, [handleWsMessage]);

  const wsStatus = useWebSocket(handleMessage);

  return (
    <AppShell wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AgentProvider>
        <CascadeApp />
      </AgentProvider>
    </ThemeProvider>
  );
}
