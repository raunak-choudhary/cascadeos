import networkx as nx


def compute_betweenness(G: nx.DiGraph) -> dict[str, float]:
    """
    Structural betweenness centrality (unweighted) so that topologically
    critical junction nodes score highest regardless of propagation speed.
    Normalised to [0, 1].
    """
    raw = nx.betweenness_centrality(G, normalized=True)

    if not raw:
        return {}

    max_val = max(raw.values()) or 1.0
    return {node_id: round(score / max_val, 4) for node_id, score in raw.items()}
