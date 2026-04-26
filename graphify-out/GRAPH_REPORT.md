# CascadeOS Knowledge Graph Report
**Updated: 2026-04-26 — Phase 0 through Phase 3**

## Summary
- **128 nodes** · **122 edges** · **27 communities**
- **6 hyperedges** capturing multi-node architectural groupings
- Phases covered: Foundation (P0), Infrastructure Graph + Map (P1), Agent Layer (P2), Cascade Engine (P3)

---

## God Nodes (Highest Connectivity)

These nodes sit at the center of the most cross-cutting relationships. Touch them carefully — changes ripple widely.

| Rank | Node | Degree | File |
|---|---|---|---|
| 1 | **BaseAgent** | 8 | `backend/agents/base_agent.py` |
| 2 | **CascadeOS System** | 7 | `CLAUDE.md` |
| 3 | **InfrastructureGraph** (spec) | 7 | `CLAUDE.md` |
| 4 | **AlertPriorityQueue** | 6 | `backend/utils/priority_queue.py` |
| 5 | **InfrastructureGraph** (code) | 5 | `backend/graph/infrastructure_graph.py` |
| 5 | **Phase 2 Agent Layer** | 5 | `CLAUDE.md` |
| 8 | **GraphContext / useGraph** | 4 | `frontend/src/context/GraphContext.jsx` |
| 8 | **SystemGraph.jsx** | 4 | `frontend/src/components/graph/SystemGraph.jsx` |
| 8 | **cascade_bfs** | 4 | `backend/graph/cascade_bfs.py` |
| 8 | **ConnectionManager** | 4 | `backend/routers/ws.py` |
| 8 | **SlidingWindow311** | 4 | `backend/data/sliding_window_311.py` |

**Key insight:** `BaseAgent` is the highest-degree node in the entire graph — the central abstraction connecting all domain agents, AlertPriorityQueue, NYC Open Data client, and WebSocket broadcast layer. Any change to its interface cascades to 4 domain agents + orchestrator.

---

## Hyperedges (Multi-Node Groupings)

| ID | Label | Members |
|---|---|---|
| `phase3_cascade_pipeline` | Phase 3 Cascade Prediction Pipeline | cascade_bfs, SimulationRouter, CascadeContext, WhatIfPanel, CascadeTimeline, CityMap |
| `phase2_real_time_stack_full` | Phase 2 Complete Real-Time Stack | AlertPriorityQueue, SlidingWindow311, ConnectionManager, BaseAgent, Orchestrator, AgentContext |
| `four_domain_agents` | Four Domain Agents | WaterAgent, TransitAgent, HealthAgent, EmergencyAgent |
| `cascade_engine_core` | Cascade Engine Core | cascade_bfs, InfrastructureGraph, SimulationRouter |
| `phase2_real_time_stack` | Phase 2 Real-Time Stack (spec) | AlertQueue, SlidingWindow, ConnectionManager, WSEvents |
| `phase1_completed` | Phase 1 Completed Components | InfrastructureGraph, betweenness, GraphContext, CityMap, SystemGraph |

---

## Surprising Cross-Cutting Connections

1. **AlertPriorityQueue ↔ SlidingWindow311 ↔ cascade_bfs** — Three different temporal data structures (max-heap, deque sliding window, BFS queue) all feed the same alert pipeline. This is the DSA showcase trifecta for the demo.

2. **SystemGraph.jsx ↔ CascadeContext** — The React Flow graph view directly consumes cascade state, mirroring CityMap during cascade events with no shared component code. Same data, two independent renderers.

3. **BaseAgent → Claude Sonnet → AlertPriorityQueue** — Every AI inference call produces structured JSON that lands in a pure-Python max-heap. The LLM output is a signal, not a display artifact.

4. **ConnectionManager** is the only node that `simulation_router`, `base_agent`, AND `orchestrator` all import — single broadcast choke point for all real-time events. If it fails, all WS event types stop.

5. **InfrastructureGraph appears twice** — once as a CLAUDE.md spec node (intent) and once as the code class (implementation). Their edges to the same neighbors confirm the spec was faithfully implemented.

---

## Community Map (27 Communities)

| Community | Representative Node | Key Members |
|---|---|---|
| Agent Core | BaseAgent | water_agent, transit_agent, health_agent, emergency_agent, orchestrator |
| Data Pipeline | AlertPriorityQueue | SlidingWindow311, nyc_open_data, alert_scorer |
| Cascade Engine | cascade_bfs | simulation_router, CascadeContext |
| Frontend Simulation | WhatIfPanel | CascadeTimeline, SimulationView |
| Map Layer | CityMap | deck.gl layers, cascade overlays |
| Graph Layer | SystemGraph | ReactFlow, NodeDetail, GraphContext |
| Agent UI | AgentPanel | AgentCard, AlertFeed, PriorityQueueViz, AgentContext |
| Infrastructure | InfrastructureGraph | betweenness, graph.py router, _centrality |
| Theme System | ThemeProvider | theme.css, ThemeToggle, useTheme |
| App Shell | AppShell | Sidebar, TopBar, StatusBar, ViewRouter |

---

## Phase Build Status

| Phase | Status | Commit | Key Abstraction |
|---|---|---|---|
| 0 — Foundation | ✅ | `fba2f70` | ThemeProvider, useWebSocket, AppShell |
| 1 — Map + Graph | ✅ | `363afce` | InfrastructureGraph (40 nodes), CityMap, SystemGraph |
| 2 — Agent Layer | ✅ | `f024cd1` | BaseAgent, AlertPriorityQueue, SlidingWindow311 |
| 3 — Cascade Engine | ✅ | `39e7caf` | cascade_bfs (26 events, ~37s), CascadeContext, SimulationView |
| 4 — Dijkstra + Briefing | 🔲 | — | dijkstra_reroute, briefing.py, RerouteLayer, CityBriefing |
| 5 — Computer Vision | 🔲 | — | YOLOv8, camera_client, CVPanel |
| 6 — Polish | 🔲 | — | keyboard shortcuts, skeleton screens, README |

---

## Query Suggestions

```
graphify query "how does an alert flow from NYC 311 to the frontend"
graphify query "what does cascade_bfs depend on"
graphify path "sliding_window_311" "agent_card"
graphify explain "base_agent"
```
