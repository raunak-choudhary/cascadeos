export function SkeletonBlock({ className = '' }) {
  return <div className={`skeleton-block ${className}`} />;
}

export function MapSkeleton({ label = 'Loading graph...' }) {
  return (
    <div className="map-placeholder">
      <div className="map-skeleton">
        <SkeletonBlock className="map-skeleton-bar map-skeleton-bar--wide" />
        <div className="map-skeleton-grid">
          {Array.from({ length: 24 }).map((_, index) => (
            <SkeletonBlock key={index} className="map-skeleton-node" />
          ))}
        </div>
        <p>{label}</p>
      </div>
    </div>
  );
}
