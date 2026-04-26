export function ComingSoon({ phase, label }) {
  return (
    <div className="coming-soon">
      <p className="coming-soon-label">{label}</p>
      <p className="coming-soon-phase">Phase {phase}</p>
    </div>
  );
}
