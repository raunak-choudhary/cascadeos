# Graph Report - .  (2026-04-26)

## Corpus Check
- Corpus is ~19,350 words - fits in a single context window. You may not need a graph.

## Summary
- 102 nodes · 90 edges · 9 communities detected
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Phase 3 Cascade Engine|Phase 3 Cascade Engine]]
- [[_COMMUNITY_Graph Algorithms|Graph Algorithms]]
- [[_COMMUNITY_Phase 1 Map & Graph|Phase 1 Map & Graph]]
- [[_COMMUNITY_Graph Algorithms|Graph Algorithms]]
- [[_COMMUNITY_Phase 2 Agent Layer|Phase 2 Agent Layer]]
- [[_COMMUNITY_Graph Algorithms|Graph Algorithms]]
- [[_COMMUNITY_Phase 3 Cascade Engine|Phase 3 Cascade Engine]]
- [[_COMMUNITY_Backend API|Backend API]]
- [[_COMMUNITY_Phase 0 Foundation|Phase 0 Foundation]]

## God Nodes (most connected - your core abstractions)
1. `CascadeOS System` - 7 edges
2. `InfrastructureGraph — 40-node NYC DiGraph` - 7 edges
3. `InfrastructureGraph` - 5 edges
4. `Phase 1 — Map and Infrastructure Graph` - 5 edges
5. `Phase 2 — Agent Layer` - 5 edges
6. `useGraph()` - 4 edges
7. `_get_centrality()` - 4 edges
8. `get_stats()` - 4 edges
9. `CityMap()` - 3 edges
10. `useTheme()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `FastAPI — async Python web framework` --implements--> `CascadeOS System`  [EXTRACTED]
  backend/requirements.txt → CLAUDE.md
- `PyTorch — deferred to Phase 5 (requirements-ml.txt)` --rationale_for--> `Phase 5 — Computer Vision Signal`  [INFERRED]
  backend/requirements-ml.txt → CLAUDE.md
- `NetworkX — graph algorithms library` --implements--> `InfrastructureGraph — 40-node NYC DiGraph`  [EXTRACTED]
  backend/requirements.txt → CLAUDE.md
- `CityMap()` --calls--> `useGraph()`  [INFERRED]
  /Users/raunakchoudhary/Data/Projects/cascadeos/frontend/src/components/map/CityMap.jsx → /Users/raunakchoudhary/Data/Projects/cascadeos/frontend/src/context/GraphContext.jsx
- `Phase 0 Implementation Units — 7 units` --rationale_for--> `Phase 0 — Foundation`  [EXTRACTED]
  docs/plans/2026-04-26-001-feat-phase-0-foundation-bootstrap-plan.md → CLAUDE.md

## Hyperedges (group relationships)
- **Cascade Engine Core Algorithms** — claude_weighted_bfs, claude_dijkstra, claude_infrastructure_graph [EXTRACTED 0.95]
- **Phase 2 Real-Time Stack** — claude_alert_queue, claude_sliding_window, claude_connection_manager, claude_ws_events [EXTRACTED 0.90]
- **Phase 1 Completed Components** — claude_infrastructure_graph, claude_betweenness, claude_deckgl, claude_reactflow, claude_graph_context [EXTRACTED 1.00]

## Communities

### Community 0 - "Phase 3 Cascade Engine"
Cohesion: 0.14
Nodes (18): Betweenness Centrality — Times Square tops at 1.0, CASCADE_PLAYBACK_SPEED env var — scales asyncio delays, CascadeOS System, deck.gl v9.3.1 — ScatterplotLayer,LineLayer,ArcLayer, Demo Origin Node — water_34th (34th St Water Main), Dijkstra Emergency Rerouting, GraphContext — shared nodes/edges/selectedNode state, InfrastructureGraph — 40-node NYC DiGraph (+10 more)

### Community 1 - "Graph Algorithms"
Cohesion: 0.18
Nodes (3): useGraph(), NodeDetail(), SystemGraph()

### Community 2 - "Phase 1 Map & Graph"
Cohesion: 0.25
Nodes (3): CityMap(), useTheme(), ThemeToggle()

### Community 3 - "Graph Algorithms"
Cohesion: 0.39
Nodes (6): compute_betweenness(), Structural betweenness centrality (unweighted) so that topologically     critica, _get_centrality(), get_edges(), get_nodes(), get_stats()

### Community 4 - "Phase 2 Agent Layer"
Cohesion: 0.29
Nodes (8): AlertPriorityQueue — Max Heap from heapq, ConnectionManager — WebSocket broadcast hub (Phase 2), LangGraph Agents — transit,water,health,emergency, NYC Open Data API — transit,water,311 complaints, Phase 2 — Agent Layer, SlidingWindow311 — 311 surge detector using deque, WebSocket Event Types — heartbeat,agent_update,alert,cascade_*, LangGraph — agent orchestration framework

### Community 5 - "Graph Algorithms"
Cohesion: 0.4
Nodes (1): InfrastructureGraph

### Community 6 - "Phase 3 Cascade Engine"
Cohesion: 0.4
Nodes (2): CascadeApp(), useWebSocket()

### Community 7 - "Backend API"
Cohesion: 0.4
Nodes (2): BaseSettings, Settings

### Community 8 - "Phase 0 Foundation"
Cohesion: 0.5
Nodes (4): Phase 0 Bootstrap Requirements R1-R15, Phase 0 — Foundation, CSS Custom Properties Theme System — dark/light, Phase 0 Implementation Units — 7 units

## Knowledge Gaps
- **15 isolated node(s):** `Structural betweenness centrality (unweighted) so that topologically     critica`, `WebSocket Event Types — heartbeat,agent_update,alert,cascade_*`, `CSS Custom Properties Theme System — dark/light`, `GraphContext — shared nodes/edges/selectedNode state`, `Demo Origin Node — water_34th (34th St Water Main)` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Graph Algorithms`** (6 nodes): `infrastructure_graph.py`, `InfrastructureGraph`, `._build()`, `.get_edges()`, `.get_nodes()`, `.__init__()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase 3 Cascade Engine`** (5 nodes): `App()`, `CascadeApp()`, `App.jsx`, `useWebSocket.js`, `useWebSocket()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend API`** (5 nodes): `config.py`, `BaseSettings`, `cors_origins_list()`, `Settings`, `validate_ml_paths()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CascadeOS System` connect `Phase 3 Cascade Engine` to `Phase 0 Foundation`, `Phase 2 Agent Layer`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Phase 2 — Agent Layer` connect `Phase 2 Agent Layer` to `Phase 3 Cascade Engine`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `Structural betweenness centrality (unweighted) so that topologically     critica`, `WebSocket Event Types — heartbeat,agent_update,alert,cascade_*`, `CSS Custom Properties Theme System — dark/light` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Phase 3 Cascade Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._