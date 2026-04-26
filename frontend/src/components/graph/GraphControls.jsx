export function GraphControls({ onFitView }) {
  return (
    <div className="graph-controls">
      <button className="map-ctrl-btn" onClick={onFitView} title="Fit to view">
        Fit
      </button>
    </div>
  );
}
