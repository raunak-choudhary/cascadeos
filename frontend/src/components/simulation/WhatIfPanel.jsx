import { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { useGraph } from '../../context/GraphContext';
import { useCascade } from '../../context/CascadeContext';

const FAILURE_TYPES = [
  { value: 'main_break',         label: 'Main Break' },
  { value: 'power_outage',       label: 'Power Outage' },
  { value: 'signal_failure',     label: 'Signal Failure' },
  { value: 'capacity_exceeded',  label: 'Capacity Exceeded' },
];

export function WhatIfPanel() {
  const { nodes } = useGraph();
  const { cascadeActive, isComplete } = useCascade();

  const [scenarios, setScenarios] = useState([]);
  const [selectedNode, setSelectedNode] = useState('water_34th');
  const [failureType, setFailureType] = useState('main_break');
  const [triggering, setTriggering] = useState(false);
  const [resetting, setResetting] = useState(false);

  useEffect(() => {
    api.getScenarios().then(setScenarios).catch(() => {});
  }, []);

  useEffect(() => {
    function handleDemoTrigger() {
      setSelectedNode('water_34th');
      setFailureType('main_break');
    }
    window.addEventListener('cascadeos:demo-trigger', handleDemoTrigger);
    return () => window.removeEventListener('cascadeos:demo-trigger', handleDemoTrigger);
  }, []);

  async function handleTrigger() {
    setTriggering(true);
    try {
      await api.triggerSimulation({ node_id: selectedNode, failure_type: failureType });
    } finally {
      setTriggering(false);
    }
  }

  async function handleReset() {
    setResetting(true);
    try {
      await api.resetSimulation();
    } finally {
      setResetting(false);
    }
  }

  function applyPreset(scenario) {
    setSelectedNode(scenario.node_id);
    setFailureType(scenario.failure_type);
  }

  return (
    <div className="whatif-panel">
      <div className="whatif-presets">
        <p className="whatif-section-label">Preset Scenarios</p>
        {scenarios.map(s => (
          <button
            key={s.id}
            className="whatif-preset-btn"
            onClick={() => applyPreset(s)}
            title={s.description}
          >
            {s.label}
          </button>
        ))}
      </div>

      <div className="whatif-controls">
        <p className="whatif-section-label">Custom Trigger</p>

        <label className="whatif-label">Origin Node</label>
        <select
          className="whatif-select"
          value={selectedNode}
          onChange={e => setSelectedNode(e.target.value)}
        >
          {nodes.map(n => (
            <option key={n.id} value={n.id}>
              {n.name} ({n.type})
            </option>
          ))}
        </select>

        <label className="whatif-label">Failure Type</label>
        <select
          className="whatif-select"
          value={failureType}
          onChange={e => setFailureType(e.target.value)}
        >
          {FAILURE_TYPES.map(f => (
            <option key={f.value} value={f.value}>{f.label}</option>
          ))}
        </select>

        <button
          className={`whatif-trigger-btn ${cascadeActive && !isComplete ? 'whatif-trigger-btn--active' : ''}`}
          onClick={handleTrigger}
          disabled={triggering || (cascadeActive && !isComplete)}
        >
          {triggering ? 'Triggering…' : cascadeActive && !isComplete ? '⚡ Cascade Running' : '⚡ Trigger Cascade'}
        </button>

        <button
          className="whatif-reset-btn"
          onClick={handleReset}
          disabled={resetting}
        >
          {resetting ? 'Resetting…' : '↺ Reset Simulation'}
        </button>
      </div>
    </div>
  );
}
