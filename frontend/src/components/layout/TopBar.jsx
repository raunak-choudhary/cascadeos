import { ThemeToggle } from '../ui/ThemeToggle';

export function TopBar({ onMenuToggle }) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <button
          className="menu-toggle"
          onClick={onMenuToggle}
          aria-label="Toggle sidebar"
        >
          <span />
          <span />
          <span />
        </button>
        <div className="topbar-brand">
          <span className="brand-name">CascadeOS</span>
          <span className="brand-tag">NYC Infrastructure Intelligence</span>
        </div>
      </div>
      <div className="topbar-right">
        <div className="status-indicator">
          <span className="status-dot live" />
          <span className="status-label">LIVE</span>
        </div>
        <ThemeToggle />
      </div>
    </header>
  );
}
