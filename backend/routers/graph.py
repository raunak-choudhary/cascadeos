from fastapi import APIRouter, Query
from graph.infrastructure_graph import graph
from graph.betweenness import compute_betweenness
from graph.dijkstra_reroute import find_emergency_reroute

router = APIRouter(prefix="/graph", tags=["graph"])

# Centrality computed once at first request and cached for the process lifetime
_centrality: dict[str, float] | None = None


def _get_centrality() -> dict[str, float]:
    global _centrality
    if _centrality is None:
        _centrality = compute_betweenness(graph.G)
    return _centrality


@router.get("/nodes")
async def get_nodes() -> list[dict]:
    centrality = _get_centrality()
    nodes = graph.get_nodes()
    for node in nodes:
        node["centrality_score"] = centrality.get(node["id"], 0.0)
    return nodes


@router.get("/edges")
async def get_edges() -> list[dict]:
    return graph.get_edges()


@router.get("/stats")
async def get_stats() -> dict:
    centrality = _get_centrality()
    nodes = graph.get_nodes()
    edges = graph.get_edges()

    by_type: dict[str, int] = {}
    for n in nodes:
        by_type[n["type"]] = by_type.get(n["type"], 0) + 1

    top_nodes = sorted(
        [{"id": n["id"], "name": n["name"], "centrality_score": centrality.get(n["id"], 0)}
         for n in nodes],
        key=lambda x: x["centrality_score"],
        reverse=True,
    )[:5]

    return {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "nodes_by_type": by_type,
        "top_centrality_nodes": top_nodes,
    }


@router.get("/reroute")
async def get_reroute(
    blocked: str = "",
    from_node: str = Query("transit_penn", alias="from"),
    to_node: str = Query("transit_grand_central", alias="to"),
) -> dict:
    blocked_nodes = [node.strip() for node in blocked.split(",") if node.strip()]
    return find_emergency_reroute(graph.G, blocked_nodes, from_node, to_node)
