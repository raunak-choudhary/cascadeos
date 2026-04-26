import { useState } from 'react';
import { Check, Copy, FileText, Loader2, X } from 'lucide-react';
import { api } from '../../services/api';

function formatAffected(systems = []) {
  return systems.map(system => (
    <li key={system.node_id}>
      <span>{system.name ?? system.node_id}</span>
      <span className="city-briefing-muted">{system.domain} · {system.status}</span>
    </li>
  ));
}

export function CityBriefing() {
  const [briefing, setBriefing] = useState(null);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const generate = async () => {
    setLoading(true);
    setError(null);
    setOpen(true);
    try {
      const data = await api.generateBriefing();
      setBriefing(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyReport = async () => {
    if (!briefing?.full_report) return;
    try {
      await navigator.clipboard.writeText(briefing.full_report);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <button
        className="city-briefing-fab"
        type="button"
        onClick={generate}
        disabled={loading}
        title="Generate City Briefing"
      >
        {loading ? <Loader2 size={18} className="city-briefing-spin" /> : <FileText size={18} />}
        <span>{loading ? 'Generating...' : 'Generate City Briefing'}</span>
      </button>

      <aside className={`city-briefing-panel ${open ? 'city-briefing-panel--open' : ''}`}>
        <div className="city-briefing-header">
          <div>
            <p className="city-briefing-kicker">City Briefing</p>
            <h2>{briefing?.incident_id ?? 'Incident Report'}</h2>
          </div>
          <button
            className="city-briefing-icon-btn"
            type="button"
            onClick={() => setOpen(false)}
            title="Close briefing"
          >
            <X size={18} />
          </button>
        </div>

        {loading && (
          <div className="city-briefing-loading">
            <Loader2 size={28} className="city-briefing-spin" />
            <span>Generating structured report...</span>
          </div>
        )}

        {error && !loading && (
          <div className="city-briefing-error">Briefing failed: {error}</div>
        )}

        {briefing && !loading && (
          <div className="city-briefing-body">
            <div className={`city-briefing-severity city-briefing-severity--${briefing.severity?.toLowerCase()}`}>
              {briefing.severity}
            </div>

            <section className="city-briefing-section">
              <h3>Summary</h3>
              <p>{briefing.summary}</p>
              <p className="city-briefing-muted">
                Generated {briefing.generated_at} · Peak impact {briefing.predicted_peak_impact}
              </p>
            </section>

            <section className="city-briefing-section">
              <h3>Cascade Origin</h3>
              <p>
                {briefing.cascade_origin?.name ?? 'No active cascade origin'}
                {briefing.cascade_origin?.node_id ? (
                  <span className="city-briefing-muted"> · {briefing.cascade_origin.node_id}</span>
                ) : null}
              </p>
            </section>

            <section className="city-briefing-section">
              <h3>Affected Systems</h3>
              <ul className="city-briefing-list">
                {briefing.affected_systems?.length ? formatAffected(briefing.affected_systems) : (
                  <li>No affected systems reported.</li>
                )}
              </ul>
            </section>

            <section className="city-briefing-section">
              <h3>Recommended Actions</h3>
              <ul className="city-briefing-list">
                {briefing.recommended_actions?.map(action => (
                  <li key={action}>{action}</li>
                ))}
              </ul>
            </section>

            {briefing.rerouting && (
              <section className="city-briefing-section">
                <h3>Rerouting</h3>
                <p>{briefing.rerouting.recommendation}</p>
                <p className="city-briefing-muted">
                  Delay {Number(briefing.rerouting.delay_minutes ?? 0).toFixed(1)} min
                </p>
              </section>
            )}

            <section className="city-briefing-section">
              <h3>Full Report</h3>
              <p className="city-briefing-report">{briefing.full_report}</p>
            </section>

            <button
              className="city-briefing-copy"
              type="button"
              onClick={copyReport}
            >
              {copied ? <Check size={16} /> : <Copy size={16} />}
              <span>{copied ? 'Copied' : 'Copy Report'}</span>
            </button>
          </div>
        )}
      </aside>
    </>
  );
}
