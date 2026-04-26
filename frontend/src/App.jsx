import { useState, useCallback } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { AppShell } from './components/layout/AppShell';
import { AgentProvider, useAgent } from './context/AgentContext';
import { CascadeProvider, useCascade } from './context/CascadeContext';
import { useWebSocket } from './hooks/useWebSocket';
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts';
import { useTheme } from './theme/ThemeProvider';

function CascadeApp() {
  const [lastHeartbeat, setLastHeartbeat] = useState(null);
  const [shortcutToast, setShortcutToast] = useState(null);
  const { handleWsMessage: agentHandler } = useAgent();
  const { handleWsMessage: cascadeHandler } = useCascade();
  const { toggleTheme } = useTheme();

  const handleMessage = useCallback((msg) => {
    if (msg.type === 'heartbeat') {
      setLastHeartbeat(msg.timestamp);
    }
    agentHandler(msg);
    cascadeHandler(msg);
  }, [agentHandler, cascadeHandler]);

  const wsStatus = useWebSocket(handleMessage);

  const handleShortcut = useCallback((message) => {
    setShortcutToast(message);
    window.setTimeout(() => setShortcutToast(null), 1800);
  }, []);

  useKeyboardShortcuts({
    toggleTheme,
    onShortcut: handleShortcut,
  });

  return (
    <>
      <AppShell wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
      {shortcutToast && <div className="shortcut-toast">{shortcutToast}</div>}
    </>
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
