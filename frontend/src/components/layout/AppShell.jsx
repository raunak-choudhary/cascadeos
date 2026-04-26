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
import { SimulationView } from '../simulation/SimulationView';
import { CityBriefing } from '../ui/CityBriefing';
import { CVPanel } from '../cv/CVPanel';

function ViewRouter({ view }) {
  switch (view) {
    case 'map':        return <CityMap />;
    case 'graph':      return <SystemGraph />;
    case 'agents':     return <AgentPanel />;
    case 'alerts':     return <AlertFeed />;
    case 'simulation': return <SimulationView />;
    case 'cv':         return <CVPanel />;
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
            {activeView === 'map' && <CityBriefing />}
            {/* NodeDetail: shared across map/graph, hidden in simulation (it has its own layout) */}
            {activeView !== 'simulation' && <NodeDetail />}
          </main>
        </div>
        <StatusBar wsStatus={wsStatus} lastHeartbeat={lastHeartbeat} />
      </div>
    </GraphProvider>
  );
}
