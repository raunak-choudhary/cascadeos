import { useState } from 'react';
import { Camera, RefreshCw } from 'lucide-react';
import { useAgent } from '../../context/AgentContext';
import { api } from '../../services/api';
import { CameraFeed } from './CameraFeed';

export function CVPanel() {
  const { cvCameras, cvDetections, cvStatus } = useAgent();
  const [polling, setPolling] = useState(false);
  const [error, setError] = useState(null);

  const refresh = async () => {
    setPolling(true);
    setError(null);
    try {
      await api.pollCv();
    } catch (err) {
      setError(err.message);
    } finally {
      setPolling(false);
    }
  };

  return (
    <div className="cv-panel">
      <div className="panel-header cv-panel-header">
        <div>
          <h2 className="panel-title">Computer Vision Signal</h2>
          <p className="panel-subtitle">NYC DOT camera frames feeding anomaly alerts into the agent layer</p>
        </div>
        <button className="cv-refresh-btn" type="button" onClick={refresh} disabled={polling}>
          <RefreshCw size={16} className={polling ? 'city-briefing-spin' : ''} />
          <span>{polling ? 'Scanning' : 'Scan Now'}</span>
        </button>
      </div>

      <div className="cv-status-row">
        <span className={`cv-status-dot cv-status-dot--${cvStatus.status ?? 'idle'}`} />
        <span>{cvStatus.message ?? `Poll interval ${30}s · Active cameras ${cvCameras.length}`}</span>
      </div>

      {error && <div className="cv-error">CV scan failed: {error}</div>}

      {cvCameras.length === 0 ? (
        <div className="cv-empty">
          <Camera size={28} />
          <p>Loading NYC DOT camera feeds...</p>
        </div>
      ) : (
        <div className="camera-grid">
          {cvCameras.slice(0, 3).map(camera => (
            <CameraFeed
              key={camera.id}
              camera={camera}
              result={cvDetections[camera.id]}
            />
          ))}
        </div>
      )}
    </div>
  );
}
