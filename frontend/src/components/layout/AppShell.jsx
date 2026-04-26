import { useState } from 'react';
import { TopBar } from './TopBar';
import { Sidebar } from './Sidebar';
import { StatusBar } from './StatusBar';

export function AppShell({ wsStatus, lastHeartbeat, children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeView, setActiveView] = useState('map');

  return (
    <div className="app-shell">
      <TopBar onMenuToggle={() => setSidebarOpen(o => !o)} />
      <div className="app-body">
        <Sidebar
          isOpen={sidebarOpen}
          activeView={activeView}
          onViewChange={setActiveView}
        />
        <main className="app-content">
          {children}
          <div className="placeholder-view">
            <p className="placeholder-label">
              Phase 0 — Foundation complete
            </p>
            <p className="placeholder-sub">
              Active view: <span className="mono">{activeView}</span>
            </p>
          </div>
        </main>
      </div>
      <StatusBar wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
    </div>
  );
}
