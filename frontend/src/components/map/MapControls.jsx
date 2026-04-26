import { RotateCcw } from 'lucide-react';

export function MapControls({ onReset }) {
  return (
    <div className="map-controls">
      <button
        className="map-ctrl-btn"
        onClick={onReset}
        title="Reset to NYC"
        aria-label="Reset map to NYC"
      >
        <RotateCcw size={16} />
      </button>
    </div>
  );
}
