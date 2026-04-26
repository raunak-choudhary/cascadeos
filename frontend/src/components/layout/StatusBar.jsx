export function StatusBar({ wsStatus, lastHeartbeat }) {
  const connected = wsStatus === 'connected';

  return (
    <div className="statusbar">
      <span className="statusbar-item">
        <span className={`status-dot ${connected ? 'live' : 'disconnected'}`} />
        <span>{connected ? 'WebSocket Connected' : 'Reconnecting…'}</span>
      </span>
      {lastHeartbeat && (
        <span className="statusbar-item statusbar-mono">
          Last heartbeat: {new Date(lastHeartbeat).toLocaleTimeString()}
        </span>
      )}
      <span className="statusbar-item statusbar-mono">CascadeOS v0.1.0</span>
    </div>
  );
}
