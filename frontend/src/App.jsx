import { useState, useCallback } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { AppShell } from './components/layout/AppShell';
import { useWebSocket } from './hooks/useWebSocket';

function CascadeApp() {
  const [lastHeartbeat, setLastHeartbeat] = useState(null);

  const handleMessage = useCallback((msg) => {
    if (msg.type === 'heartbeat') {
      setLastHeartbeat(msg.timestamp);
      console.log('[WS] heartbeat', msg.timestamp);
    }
  }, []);

  const wsStatus = useWebSocket(handleMessage);

  return (
    <AppShell wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <CascadeApp />
    </ThemeProvider>
  );
}
