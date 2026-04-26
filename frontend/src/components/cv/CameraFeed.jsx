import { AlertTriangle, Camera } from 'lucide-react';
import { api } from '../../services/api';

const CLASS_LABELS = {
  congestion: 'Congestion',
  stalled_vehicle: 'Stalled vehicle',
  crowd_density: 'Crowd density',
  potential_flooding: 'Potential flooding',
};

export function CameraFeed({ camera, result }) {
  const detections = result?.detections ?? [];
  const frameUrl = result?.frame_url
    ? `${api.baseUrl}${result.frame_url}`
    : api.cvFrameUrl(camera.id);
  const width = result?.frame_width ?? 640;
  const height = result?.frame_height ?? 360;

  return (
    <article className={`camera-feed ${result?.anomaly_detected ? 'camera-feed--anomaly' : ''}`}>
      <div className="camera-feed-header">
        <div>
          <h3>{camera.name}</h3>
          <p>{Number(camera.lat).toFixed(4)}, {Number(camera.lng).toFixed(4)}</p>
        </div>
        {result?.anomaly_detected ? (
          <span className="camera-anomaly-banner">
            <AlertTriangle size={14} />
            ANOMALY DETECTED
          </span>
        ) : (
          <span className="camera-model-badge">{result?.model_status ?? 'waiting'}</span>
        )}
      </div>

      <div className="camera-frame-wrap">
        <img className="camera-frame" src={frameUrl} alt={`${camera.name} latest frame`} />
        <svg className="camera-box-overlay" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
          {detections.map((detection, index) => {
            const [x1, y1, x2, y2] = detection.bbox;
            return (
              <g key={`${detection.class}-${index}`} className={`camera-box camera-box--${detection.class}`}>
                <rect x={x1} y={y1} width={Math.max(1, x2 - x1)} height={Math.max(1, y2 - y1)} />
                <text x={x1 + 4} y={Math.max(14, y1 + 14)}>
                  {CLASS_LABELS[detection.class] ?? detection.class} {Math.round(detection.confidence * 100)}%
                </text>
              </g>
            );
          })}
        </svg>
        {detections.length === 0 && (
          <div className="camera-frame-empty">
            <Camera size={18} />
            <span>No detections on latest frame</span>
          </div>
        )}
      </div>

      <div className="camera-feed-footer">
        <span>Severity {Number(result?.overall_severity ?? 0).toFixed(1)}</span>
        <span>{result?.frame_timestamp ? new Date(result.frame_timestamp).toLocaleTimeString() : 'Waiting for frame'}</span>
      </div>
    </article>
  );
}
