"""
Weighted BFS cascade propagation engine.
Implemented from scratch using collections.deque — no networkx traversal helpers.

Propagation time model:
  time = current_time + (1.0 / edge_weight) * base_minutes
  base_minutes = 5.0 same-domain, 12.0 cross-domain

Severity decays with cascade depth so downstream nodes are less impacted.
"""
from collections import deque
from datetime import datetime, timezone
from typing import Any

import networkx as nx

BASE_SAME_DOMAIN = 5.0    # minutes to propagate within same infrastructure domain
BASE_CROSS_DOMAIN = 12.0  # minutes to propagate across domain boundaries
MAX_DEPTH = 6             # cap BFS depth to keep demo timeline readable


def cascade_bfs(
    graph: nx.DiGraph,
    origin_node_id: str,
    failure_time: datetime | None = None,
) -> list[dict[str, Any]]:
    """
    Run weighted BFS from origin_node_id across the infrastructure graph.

    Returns a list of cascade event dicts sorted by predicted_impact_minutes.
    The origin node itself is included at depth 0 / 0.0 minutes.
    """
    if failure_time is None:
        failure_time = datetime.now(timezone.utc)

    if origin_node_id not in graph:
        return []

    origin_type = graph.nodes[origin_node_id].get("type", "unknown")

    visited: set[str] = set()
    queue: deque[dict] = deque()
    results: list[dict] = []

    queue.append({
        "node_id": origin_node_id,
        "time_minutes": 0.0,
        "path": [origin_node_id],
        "depth": 0,
        "severity": 1.0,
    })

    while queue:
        current = queue.popleft()
        node_id = current["node_id"]

        if node_id in visited:
            continue
        visited.add(node_id)

        node_data = dict(graph.nodes[node_id])
        current_severity = current["severity"]

        results.append({
            "node_id":                  node_id,
            "domain":                   node_data.get("type", "unknown"),
            "node_name":                node_data.get("name", node_id),
            "predicted_impact_minutes": round(current["time_minutes"], 2),
            "severity":                 round(current_severity, 3),
            "propagation_path":         current["path"],
            "cascade_depth":            current["depth"],
        })

        if current["depth"] >= MAX_DEPTH:
            continue

        for neighbor in graph.successors(node_id):
            if neighbor in visited:
                continue

            edge_data = graph[node_id][neighbor]
            weight = max(0.05, float(edge_data.get("weight", 0.5)))
            neighbor_type = graph.nodes[neighbor].get("type", "unknown")

            base = BASE_SAME_DOMAIN if neighbor_type == origin_type else BASE_CROSS_DOMAIN
            propagation_minutes = current["time_minutes"] + (1.0 / weight) * base

            # Severity decays: 15 % per depth level, floored at 0.1
            child_severity = max(0.1, current_severity * 0.85)

            queue.append({
                "node_id":      neighbor,
                "time_minutes": propagation_minutes,
                "path":         current["path"] + [neighbor],
                "depth":        current["depth"] + 1,
                "severity":     child_severity,
            })

    return sorted(results, key=lambda x: x["predicted_impact_minutes"])
