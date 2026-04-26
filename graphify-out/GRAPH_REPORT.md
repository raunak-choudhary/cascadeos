# Graph Report - cascadeos  (2026-04-26)

## Corpus Check
- 65 files · ~30,022 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 306 nodes · 380 edges · 20 communities detected
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 78 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]

## God Nodes (most connected - your core abstractions)
1. `AlertPriorityQueue` - 13 edges
2. `BaseAgent` - 11 edges
3. `run_orchestrator()` - 11 edges
4. `start_background_agents()` - 9 edges
5. `generate_briefing()` - 9 edges
6. `poll_cv_once()` - 8 edges
7. `CameraClient` - 8 edges
8. `useAgent()` - 7 edges
9. `fetch_311_complaints()` - 7 edges
10. `CascadeOS System` - 7 edges

## Surprising Connections (you probably didn't know these)
- `generate_briefing()` --calls--> `get_last_reroute()`  [INFERRED]
  backend/routers/briefing.py → backend/graph/dijkstra_reroute.py
- `CascadeOS System` --implements--> `FastAPI — async Python web framework`  [EXTRACTED]
  CLAUDE.md → backend/requirements.txt
- `Phase 5 — Computer Vision Signal` --rationale_for--> `PyTorch — deferred to Phase 5 (requirements-ml.txt)`  [INFERRED]
  CLAUDE.md → backend/requirements-ml.txt
- `InfrastructureGraph — 40-node NYC DiGraph` --implements--> `NetworkX — graph algorithms library`  [EXTRACTED]
  CLAUDE.md → backend/requirements.txt
- `CascadeApp()` --calls--> `useCascade()`  [INFERRED]
  frontend/src/App.jsx → frontend/src/context/CascadeContext.jsx

## Hyperedges (group relationships)
- **Cascade Engine Core Algorithms** — claude_weighted_bfs, claude_dijkstra, claude_infrastructure_graph [EXTRACTED 0.95]
- **Phase 2 Real-Time Stack** — claude_alert_queue, claude_sliding_window, claude_connection_manager, claude_ws_events [EXTRACTED 0.90]
- **Phase 1 Completed Components** — claude_infrastructure_graph, claude_betweenness, claude_deckgl, claude_reactflow, claude_graph_context [EXTRACTED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (30): Phase 0 Bootstrap Requirements R1-R15, AlertPriorityQueue — Max Heap from heapq, Betweenness Centrality — Times Square tops at 1.0, CASCADE_PLAYBACK_SPEED env var — scales asyncio delays, CascadeOS System, ConnectionManager — WebSocket broadcast hub (Phase 2), deck.gl v9.3.1 — ScatterplotLayer,LineLayer,ArcLayer, Demo Origin Node — water_34th (34th St Water Main) (+22 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (18): BaseAgent, EmergencyAgent, HealthAgent, Launch all domain agents + orchestrator as background asyncio tasks., start_background_agents(), fetch_311_complaints(), fetch_fdny_incidents(), fetch_hospital_capacity() (+10 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (10): useCascade(), CascadeTimeline(), CityMap(), useGraph(), NodeDetail(), buildRFNode(), cascadeBorderColor(), geoToCanvas() (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (10): useAgent(), AgentPanel(), AlertFeed(), CascadeApp(), CVPanel(), PriorityQueueViz(), useTheme(), ThemeToggle() (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (12): _prune_stale(), Coordinator agent — pops from the shared AlertPriorityQueue, decides if multiple, Background loop — pop alerts, check for cascade, run 311 window., run_orchestrator(), Return and remove the highest-priority alert. Returns None if empty., 311 surge detector — sliding window implemented with collections.deque. Evicts c, Add new complaints. Evict stale entries older than window_seconds., Return neighborhoods currently in surge with severity score. (+4 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (10): BaseAgent, _now_iso(), BaseAgent — shared interface for all four domain agents. Each agent fetches live, Continuous polling loop — call this as an asyncio task., broadcast_fn is manager.broadcast from routers/ws.py., Send data summary to Claude Sonnet, return structured reasoning JSON., AlertPriorityQueue, Max-heap alert priority queue implemented from scratch using Python's heapq. hea (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.13
Nodes (15): BaseModel, cascade_bfs(), Weighted BFS cascade propagation engine. Implemented from scratch using collecti, Run weighted BFS from origin_node_id across the infrastructure graph.      Retur, clear_last_reroute(), get_node_status(), _now_iso(), Simulation router — triggers cascade BFS, streams results over WebSocket, resets (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.18
Nodes (11): _emit_cv_alert(), get_cameras(), get_latest_frame(), _now_iso(), poll_cv_once(), poll_now(), Computer vision camera endpoints and polling loop., run_cv_monitor() (+3 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (15): compute_betweenness(), Structural betweenness centrality (unweighted) so that topologically     critica, find_emergency_reroute(), _generate_recommendation(), get_last_reroute(), _node_name(), _path_cost_minutes(), Dijkstra emergency rerouting over the infrastructure graph.  NetworkX provides t (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.23
Nodes (6): CameraClient, _flatten_camera_payload(), _float_or_none(), _now(), _pick(), NYC DOT traffic camera client with a small in-memory frame cache.

### Community 10 - "Community 10"
Cohesion: 0.39
Nodes (7): Push an alert with a severity priority (0.0–10.0). Higher = processed first., buildRerouteLayers(), cssColor(), dashPairs(), hexToRgba(), interpolate(), pairsForPath()

### Community 11 - "Community 11"
Cohesion: 0.42
Nodes (8): _affected_systems(), _cascade_origin(), _fallback_briefing(), generate_briefing(), _now(), _parse_json_response(), City briefing generation for current cascade state., _severity()

### Community 12 - "Community 12"
Cohesion: 0.4
Nodes (1): InfrastructureGraph

### Community 13 - "Community 13"
Cohesion: 0.4
Nodes (2): BaseSettings, Settings

### Community 14 - "Community 14"
Cohesion: 0.5
Nodes (3): Utility to compute a composite severity score for raw alert signals., Returns a severity score 0.0–10.0.     - base: domain baseline     - volume bonu, score_alert()

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (2): CityBriefing(), formatAffected()

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Computer vision integrations for CascadeOS.

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (2): Codex Handoff Phase 4, Phase 3 Cascade Engine

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Phase 2 Agent Layer

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): WebSocket Event Protocol

## Knowledge Gaps
- **48 isolated node(s):** `Simulation router — triggers cascade BFS, streams results over WebSocket, resets`, `Run BFS and stream cascade_node events with time-scaled delays.`, `Returns the current runtime status overrides for all affected nodes.`, `Broadcast server — all connected clients receive every event.`, `Computer vision camera endpoints and polling loop.` (+43 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (6 nodes): `infrastructure_graph.py`, `InfrastructureGraph`, `._build()`, `.get_edges()`, `.get_nodes()`, `.__init__()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (5 nodes): `config.py`, `BaseSettings`, `cors_origins_list()`, `Settings`, `validate_ml_paths()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (3 nodes): `CityBriefing()`, `formatAffected()`, `CityBriefing.jsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `__init__.py`, `Computer vision integrations for CascadeOS.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `Codex Handoff Phase 4`, `Phase 3 Cascade Engine`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `Phase 2 Agent Layer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `WebSocket Event Protocol`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_orchestrator()` connect `Community 4` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `AlertPriorityQueue` connect `Community 5` to `Community 10`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `generate_briefing()` connect `Community 11` to `Community 8`, `Community 5`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `AlertPriorityQueue` (e.g. with `BaseAgent` and `BaseAgent — shared interface for all four domain agents. Each agent fetches live`) actually correct?**
  _`AlertPriorityQueue` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `BaseAgent` (e.g. with `HealthAgent` and `AlertPriorityQueue`) actually correct?**
  _`BaseAgent` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `run_orchestrator()` (e.g. with `start_background_agents()` and `.size()`) actually correct?**
  _`run_orchestrator()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `start_background_agents()` (e.g. with `WaterAgent` and `TransitAgent`) actually correct?**
  _`start_background_agents()` has 7 INFERRED edges - model-reasoned connections that need verification._