"""
Dijkstra emergency rerouting over the infrastructure graph.

NetworkX provides the traversal; this module only adapts cascade edge weights
into route costs and stores the latest recommendation for briefing generation.
"""
from __future__ import annotations

import json
from typing import Any

import anthropic
import networkx as nx

from config import settings

ROUTE_COST_MINUTES = 5.0

_anthropic = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
_last_reroute: dict[str, Any] | None = None


def _node_name(graph: nx.DiGraph, node_id: str) -> str:
    return graph.nodes[node_id].get("name", node_id) if node_id in graph else node_id


def _route_graph(source_graph: nx.DiGraph, blocked_nodes: set[str]) -> nx.DiGraph:
    available = [node for node in source_graph.nodes if node not in blocked_nodes]
    routed = source_graph.subgraph(available).copy()
    for _, _, data in routed.edges(data=True):
        speed = max(0.05, float(data.get("weight", 0.5)))
        data["route_speed"] = speed
        data["weight"] = 1.0 / speed
    return routed


def _path_cost_minutes(graph: nx.DiGraph, path: list[str]) -> float:
    total = 0.0
    for source, target in zip(path, path[1:]):
        speed = max(0.05, float(graph[source][target].get("weight", 0.5)))
        total += (1.0 / speed) * ROUTE_COST_MINUTES
    return round(total, 2)


def _generate_recommendation(
    graph: nx.DiGraph,
    blocked_nodes: list[str],
    original_path: list[str],
    rerouted_path: list[str],
    delay_minutes: float,
) -> str:
    blocked_names = [_node_name(graph, node_id) for node_id in blocked_nodes]
    payload = {
        "blocked_nodes": blocked_names,
        "original_path": [_node_name(graph, node_id) for node_id in original_path],
        "rerouted_path": [_node_name(graph, node_id) for node_id in rerouted_path],
        "delay_minutes": delay_minutes,
    }
    prompt = (
        "Generate 1-2 concise operational sentences for NYC emergency routing. "
        "Mention the blocked corridor, the reroute, and the added delay.\n"
        f"{json.dumps(payload, indent=2)}"
    )
    try:
        message = _anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=160,
            system=(
                "You are an emergency transportation coordinator for New York City. "
                "Be concise, factual, and actionable."
            ),
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except Exception:
        reroute_names = " -> ".join(payload["rerouted_path"])
        blocked = ", ".join(blocked_names) or "the impacted corridor"
        return (
            f"Avoid {blocked}. Route emergency movement via {reroute_names}; "
            f"estimated added delay is {delay_minutes:.1f} minutes."
        )


def find_emergency_reroute(
    graph: nx.DiGraph,
    blocked_nodes: list[str],
    origin: str,
    destination: str,
) -> dict[str, Any]:
    """
    Run Dijkstra on the infrastructure graph excluding blocked_nodes.

    Cascade edge weight means propagation speed, so the route graph inverts
    that value before calling NetworkX's nx.dijkstra_path with weight='weight'.
    """
    global _last_reroute

    if origin not in graph:
        raise ValueError(f"Origin node '{origin}' not found in graph")
    if destination not in graph:
        raise ValueError(f"Destination node '{destination}' not found in graph")

    blocked_set = set(blocked_nodes) - {origin, destination}
    original_graph = _route_graph(graph, set())
    reroute_graph = _route_graph(graph, blocked_set)

    original_path = nx.dijkstra_path(
        original_graph,
        source=origin,
        target=destination,
        weight="weight",
    )
    rerouted_path = nx.dijkstra_path(
        reroute_graph,
        source=origin,
        target=destination,
        weight="weight",
    )

    original_cost = _path_cost_minutes(graph, original_path)
    rerouted_cost = _path_cost_minutes(graph, rerouted_path)
    delay = round(max(0.0, rerouted_cost - original_cost), 2)
    recommendation = _generate_recommendation(
        graph,
        sorted(blocked_set),
        original_path,
        rerouted_path,
        delay,
    )

    _last_reroute = {
        "original_path": original_path,
        "rerouted_path": rerouted_path,
        "blocked_nodes": sorted(blocked_set),
        "origin": origin,
        "destination": destination,
        "original_cost_minutes": original_cost,
        "rerouted_cost_minutes": rerouted_cost,
        "delay_minutes": delay,
        "recommendation": recommendation,
    }
    return _last_reroute


def get_last_reroute() -> dict[str, Any] | None:
    return _last_reroute


def clear_last_reroute() -> None:
    global _last_reroute
    _last_reroute = None
