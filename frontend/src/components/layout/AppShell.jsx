import { useState } from 'react';
import { TopBar } from './TopBar';
import { Sidebar } from './Sidebar';
import { StatusBar } from './StatusBar';
import { GraphProvider } from '../../context/GraphContext';
import { CityMap } from '../map/CityMap';
import { SystemGraph } from '../graph/SystemGraph';
import { NodeDetail } from '../graph/NodeDetail';
import { AgentPanel } from '../agents/AgentPanel';
import { AlertFeed } from '../agents/AlertFeed';
import { PriorityQueueViz } from '../ui/PriorityQueue';
import { ComingSoon } from '../ui/ComingSoon';

function ViewRouter({ view }) {
  switch (view) {
    case 'map':        return <CityMap />;
    case 'graph':      return <SystemGraph />;
    case 'agents':     return <AgentPanel />;
    case 'alerts':     return <AlertFeed />;
    case 'simulation': return <ComingSoon label="Cascade Simulator" phase={3} />;
    case 'cv':         return <ComingSoon label="Computer Vision Feeds" phase={5} />;
    default:           return <CityMap />;
  }
}

export function AppShell({ wsStatus, lastHeartbeat }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeView, setActiveView] = useState('map');

  return (
    <GraphProvider>
      <div className="app-shell">
        <TopBar onMenuToggle={() => setSidebarOpen(o => !o)} />
        <div className="app-body">
          <Sidebar
            isOpen={sidebarOpen}
            activeView={activeView}
            onViewChange={setActiveView}
          />
          <main className="app-content">
            <ViewRouter view={activeView} />
            {/* NodeDetail shared across map/graph views */}
            <NodeDetail />
          </main>
        </div>
        <StatusBar wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
      </div>
    </GraphProvider>
  );
}
