import { CityMap } from '../map/CityMap';
import { WhatIfPanel } from './WhatIfPanel';
import { CascadeTimeline } from './CascadeTimeline';

export function SimulationView() {
  return (
    <div className="simulation-view">
      <div className="simulation-map-area">
        <CityMap />
      </div>
      <aside className="simulation-sidebar">
        <WhatIfPanel />
        <CascadeTimeline />
      </aside>
    </div>
  );
}
