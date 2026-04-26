import { Map, GitFork, Activity, Radio, Camera, Zap } from 'lucide-react';

const NAV_ITEMS = [
  { id: 'map',        label: 'City Map',   icon: Map },
  { id: 'graph',      label: 'Sys Graph',  icon: GitFork },
  { id: 'agents',     label: 'Agents',     icon: Activity },
  { id: 'simulation', label: 'Simulate',   icon: Zap },
  { id: 'cv',         label: 'CV Feeds',   icon: Camera },
  { id: 'alerts',     label: 'Alerts',     icon: Radio },
];

export function Sidebar({ isOpen, activeView, onViewChange }) {
  return (
    <aside className={`sidebar ${isOpen ? 'sidebar--open' : 'sidebar--closed'}`}>
      <nav className="sidebar-nav">
        {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            className={`nav-item ${activeView === id ? 'nav-item--active' : ''}`}
            onClick={() => onViewChange(id)}
            aria-label={label}
          >
            <Icon size={20} />
            <span className="nav-label">{label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}
