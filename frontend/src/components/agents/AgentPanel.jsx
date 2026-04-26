import { useAgent } from '../../context/AgentContext';
import { AgentCard } from './AgentCard';
import { PriorityQueueViz } from '../ui/PriorityQueue';

export function AgentPanel() {
  const { agents } = useAgent();

  return (
    <div className="agent-panel">
      <div className="panel-header">
        <h2 className="panel-title">Agent Layer</h2>
        <p className="panel-subtitle">Four LangGraph agents monitoring NYC infrastructure in real time</p>
      </div>

      <div className="agent-grid">
        {Object.values(agents).map(agent => (
          <AgentCard key={agent.domain} agent={agent} />
        ))}
      </div>

      <PriorityQueueViz />
    </div>
  );
}
