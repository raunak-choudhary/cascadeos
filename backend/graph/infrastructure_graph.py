import networkx as nx
from typing import Any

# ---------------------------------------------------------------------------
# Node definitions — real NYC coordinates
# ---------------------------------------------------------------------------

_RAW_NODES: list[dict[str, Any]] = [
    # ── Water ──────────────────────────────────────────────────────────────
    {
        "id": "water_34th",
        "type": "water",
        "name": "34th St Water Main",
        "lat": 40.7484,
        "lng": -73.9967,
        "capacity": 0.71,
        "status": "normal",
    },
    {
        "id": "water_42nd",
        "type": "water",
        "name": "42nd St Water Junction",
        "lat": 40.7549,
        "lng": -73.9840,
        "capacity": 0.58,
        "status": "normal",
    },
    {
        "id": "water_125th",
        "type": "water",
        "name": "125th St Harlem Main",
        "lat": 40.8048,
        "lng": -73.9507,
        "capacity": 0.62,
        "status": "normal",
    },
    {
        "id": "water_uptown",
        "type": "water",
        "name": "Upper West Side Main",
        "lat": 40.7831,
        "lng": -73.9712,
        "capacity": 0.55,
        "status": "normal",
    },
    {
        "id": "water_lower_east",
        "type": "water",
        "name": "Lower East Side Junction",
        "lat": 40.7143,
        "lng": -73.9855,
        "capacity": 0.48,
        "status": "normal",
    },
    {
        "id": "water_brooklyn_hts",
        "type": "water",
        "name": "Brooklyn Heights Pump Station",
        "lat": 40.6954,
        "lng": -73.9952,
        "capacity": 0.67,
        "status": "normal",
    },
    {
        "id": "water_brooklyn_atl",
        "type": "water",
        "name": "Atlantic Ave Water Main",
        "lat": 40.6845,
        "lng": -73.9773,
        "capacity": 0.73,
        "status": "warning",
    },
    {
        "id": "water_queens_jax",
        "type": "water",
        "name": "Jackson Heights Water Junction",
        "lat": 40.7477,
        "lng": -73.8908,
        "capacity": 0.44,
        "status": "normal",
    },
    {
        "id": "water_bronx_hunts",
        "type": "water",
        "name": "Hunts Point Water Main",
        "lat": 40.8143,
        "lng": -73.8930,
        "capacity": 0.51,
        "status": "normal",
    },
    {
        "id": "water_staten",
        "type": "water",
        "name": "Staten Island North Shore Main",
        "lat": 40.6401,
        "lng": -74.0766,
        "capacity": 0.39,
        "status": "normal",
    },
    # ── Transit ────────────────────────────────────────────────────────────
    {
        "id": "transit_34th_herald",
        "type": "transit",
        "name": "34th St-Herald Square",
        "lat": 40.7484,
        "lng": -73.9879,
        "capacity": 0.82,
        "status": "warning",
    },
    {
        "id": "transit_penn",
        "type": "transit",
        "name": "Penn Station-34th St",
        "lat": 40.7505,
        "lng": -73.9934,
        "capacity": 0.76,
        "status": "normal",
    },
    {
        "id": "transit_times_sq",
        "type": "transit",
        "name": "Times Square-42nd St",
        "lat": 40.7580,
        "lng": -73.9855,
        "capacity": 0.88,
        "status": "warning",
    },
    {
        "id": "transit_grand_central",
        "type": "transit",
        "name": "Grand Central-42nd St",
        "lat": 40.7527,
        "lng": -73.9772,
        "capacity": 0.79,
        "status": "normal",
    },
    {
        "id": "transit_59th",
        "type": "transit",
        "name": "59th St-Columbus Circle",
        "lat": 40.7681,
        "lng": -73.9819,
        "capacity": 0.61,
        "status": "normal",
    },
    {
        "id": "transit_union_sq",
        "type": "transit",
        "name": "Union Square-14th St",
        "lat": 40.7352,
        "lng": -73.9896,
        "capacity": 0.74,
        "status": "normal",
    },
    {
        "id": "transit_14th_8th",
        "type": "transit",
        "name": "14th St-8th Ave",
        "lat": 40.7402,
        "lng": -74.0006,
        "capacity": 0.57,
        "status": "normal",
    },
    {
        "id": "transit_fulton",
        "type": "transit",
        "name": "Fulton St",
        "lat": 40.7092,
        "lng": -74.0077,
        "capacity": 0.69,
        "status": "normal",
    },
    {
        "id": "transit_125th",
        "type": "transit",
        "name": "125th St Station",
        "lat": 40.8048,
        "lng": -73.9455,
        "capacity": 0.63,
        "status": "normal",
    },
    {
        "id": "transit_atlantic",
        "type": "transit",
        "name": "Atlantic Av-Barclays Center",
        "lat": 40.6843,
        "lng": -73.9773,
        "capacity": 0.77,
        "status": "normal",
    },
    {
        "id": "transit_borough_hall",
        "type": "transit",
        "name": "Borough Hall",
        "lat": 40.6926,
        "lng": -73.9898,
        "capacity": 0.55,
        "status": "normal",
    },
    {
        "id": "transit_jackson_hts",
        "type": "transit",
        "name": "Jackson Heights-Roosevelt Ave",
        "lat": 40.7477,
        "lng": -73.8908,
        "capacity": 0.68,
        "status": "normal",
    },
    # ── Health ─────────────────────────────────────────────────────────────
    {
        "id": "health_nyu",
        "type": "health",
        "name": "NYU Langone Medical Center",
        "lat": 40.7421,
        "lng": -73.9739,
        "capacity": 0.78,
        "status": "warning",
    },
    {
        "id": "health_bellevue",
        "type": "health",
        "name": "Bellevue Hospital Center",
        "lat": 40.7394,
        "lng": -73.9757,
        "capacity": 0.85,
        "status": "warning",
    },
    {
        "id": "health_mount_sinai",
        "type": "health",
        "name": "Mount Sinai Hospital",
        "lat": 40.7900,
        "lng": -73.9525,
        "capacity": 0.66,
        "status": "normal",
    },
    {
        "id": "health_presbyterian",
        "type": "health",
        "name": "NewYork-Presbyterian/Columbia",
        "lat": 40.8399,
        "lng": -73.9416,
        "capacity": 0.71,
        "status": "normal",
    },
    {
        "id": "health_kings_county",
        "type": "health",
        "name": "Kings County Hospital",
        "lat": 40.6552,
        "lng": -73.9440,
        "capacity": 0.82,
        "status": "warning",
    },
    {
        "id": "health_maimonides",
        "type": "health",
        "name": "Maimonides Medical Center",
        "lat": 40.6376,
        "lng": -73.9976,
        "capacity": 0.59,
        "status": "normal",
    },
    {
        "id": "health_jamaica",
        "type": "health",
        "name": "Jamaica Hospital Medical Center",
        "lat": 40.6990,
        "lng": -73.8024,
        "capacity": 0.64,
        "status": "normal",
    },
    {
        "id": "health_lincoln",
        "type": "health",
        "name": "Lincoln Hospital",
        "lat": 40.8157,
        "lng": -73.9233,
        "capacity": 0.70,
        "status": "normal",
    },
    {
        "id": "health_elmhurst",
        "type": "health",
        "name": "Elmhurst Hospital Center",
        "lat": 40.7399,
        "lng": -73.8836,
        "capacity": 0.75,
        "status": "normal",
    },
    # ── Emergency ──────────────────────────────────────────────────────────
    {
        "id": "emrg_fdny_downtown",
        "type": "emergency",
        "name": "FDNY Engine 1 Downtown Manhattan",
        "lat": 40.7201,
        "lng": -74.0048,
        "capacity": 0.45,
        "status": "normal",
    },
    {
        "id": "emrg_fdny_midtown",
        "type": "emergency",
        "name": "FDNY Engine 7 Midtown",
        "lat": 40.7547,
        "lng": -73.9877,
        "capacity": 0.52,
        "status": "normal",
    },
    {
        "id": "emrg_fdny_harlem",
        "type": "emergency",
        "name": "FDNY Engine 58 Harlem",
        "lat": 40.8031,
        "lng": -73.9505,
        "capacity": 0.41,
        "status": "normal",
    },
    {
        "id": "emrg_fdny_brooklyn",
        "type": "emergency",
        "name": "FDNY Engine 201 Brooklyn",
        "lat": 40.6865,
        "lng": -73.9820,
        "capacity": 0.48,
        "status": "normal",
    },
    {
        "id": "emrg_nypd_midtown",
        "type": "emergency",
        "name": "NYPD 17th Precinct Midtown East",
        "lat": 40.7556,
        "lng": -73.9692,
        "capacity": 0.60,
        "status": "normal",
    },
    {
        "id": "emrg_nypd_brooklyn",
        "type": "emergency",
        "name": "NYPD 77th Precinct Brooklyn",
        "lat": 40.6725,
        "lng": -73.9445,
        "capacity": 0.55,
        "status": "normal",
    },
    {
        "id": "emrg_nypd_harlem",
        "type": "emergency",
        "name": "NYPD 26th Precinct Harlem",
        "lat": 40.8109,
        "lng": -73.9525,
        "capacity": 0.43,
        "status": "normal",
    },
    {
        "id": "emrg_oem",
        "type": "emergency",
        "name": "NYC Office of Emergency Management",
        "lat": 40.7114,
        "lng": -74.0120,
        "capacity": 0.50,
        "status": "normal",
    },
    {
        "id": "emrg_ems_manhattan",
        "type": "emergency",
        "name": "NYC EMS Station 1 Manhattan",
        "lat": 40.7423,
        "lng": -74.0021,
        "capacity": 0.58,
        "status": "normal",
    },
]


# ---------------------------------------------------------------------------
# Edge definitions — (source, target, attrs)
# weight = propagation speed 0.1–1.0 (higher = faster cascade)
# type   = "dependency" | "proximity" | "operational"
# ---------------------------------------------------------------------------

_RAW_EDGES: list[tuple[str, str, dict[str, Any]]] = [
    # ── Water intra-domain ──────────────────────────────────────────────────
    ("water_34th",        "water_42nd",         {"weight": 0.8, "type": "dependency",   "bidirectional": True}),
    ("water_42nd",        "water_125th",        {"weight": 0.7, "type": "dependency",   "bidirectional": True}),
    ("water_125th",       "water_uptown",       {"weight": 0.75,"type": "dependency",   "bidirectional": True}),
    ("water_34th",        "water_lower_east",   {"weight": 0.7, "type": "dependency",   "bidirectional": True}),
    ("water_lower_east",  "water_brooklyn_hts", {"weight": 0.5, "type": "dependency",   "bidirectional": True}),
    ("water_brooklyn_hts","water_brooklyn_atl", {"weight": 0.8, "type": "dependency",   "bidirectional": True}),
    ("water_125th",       "water_bronx_hunts",  {"weight": 0.6, "type": "dependency",   "bidirectional": True}),

    # ── Transit intra-domain — subway lines ─────────────────────────────────
    # A/C/E line fragment
    ("transit_14th_8th",  "transit_34th_herald",{"weight": 0.9, "type": "operational",  "bidirectional": True}),
    ("transit_34th_herald","transit_penn",       {"weight": 0.9, "type": "operational",  "bidirectional": True}),
    ("transit_penn",      "transit_times_sq",   {"weight": 0.9, "type": "operational",  "bidirectional": True}),
    ("transit_times_sq",  "transit_59th",       {"weight": 0.85,"type": "operational",  "bidirectional": True}),
    # 4/5/6 line fragment
    ("transit_union_sq",  "transit_grand_central",{"weight": 0.9,"type": "operational", "bidirectional": True}),
    ("transit_grand_central","transit_times_sq",{"weight": 0.85,"type": "proximity",    "bidirectional": True}),
    ("transit_grand_central","transit_59th",    {"weight": 0.8, "type": "operational",  "bidirectional": True}),
    # 14th St crosstown L corridor — emergency fallback when Times Sq is blocked
    ("transit_14th_8th",  "transit_union_sq",   {"weight": 0.75,"type": "operational",  "bidirectional": True}),
    # 2/3 line fragment
    ("transit_fulton",    "transit_union_sq",   {"weight": 0.85,"type": "operational",  "bidirectional": True}),
    ("transit_union_sq",  "transit_times_sq",   {"weight": 0.8, "type": "operational",  "bidirectional": True}),
    ("transit_times_sq",  "transit_125th",      {"weight": 0.75,"type": "operational",  "bidirectional": True}),
    # Brooklyn connections
    ("transit_fulton",    "transit_borough_hall",{"weight": 0.85,"type":"operational",  "bidirectional": True}),
    ("transit_borough_hall","transit_atlantic",  {"weight": 0.8, "type": "operational", "bidirectional": True}),
    # Emergency services within domain
    ("emrg_fdny_midtown", "emrg_nypd_midtown",  {"weight": 0.7, "type": "operational", "bidirectional": True}),
    ("emrg_fdny_harlem",  "emrg_nypd_harlem",   {"weight": 0.7, "type": "operational", "bidirectional": True}),
    ("emrg_fdny_brooklyn","emrg_nypd_brooklyn",  {"weight": 0.7, "type": "operational", "bidirectional": True}),
    ("emrg_oem",          "emrg_ems_manhattan",  {"weight": 0.9, "type": "operational", "bidirectional": True}),
    ("emrg_oem",          "emrg_fdny_downtown",  {"weight": 0.8, "type": "operational", "bidirectional": True}),
    ("emrg_oem",          "emrg_fdny_midtown",   {"weight": 0.8, "type": "operational", "bidirectional": True}),

    # ── Cross-domain: water → transit (flooding risk) ────────────────────────
    ("water_34th",        "transit_34th_herald", {"weight": 0.7, "type": "proximity",   "bidirectional": False}),
    ("water_34th",        "transit_penn",        {"weight": 0.65,"type": "proximity",   "bidirectional": False}),
    ("water_42nd",        "transit_times_sq",    {"weight": 0.7, "type": "proximity",   "bidirectional": False}),
    ("water_42nd",        "transit_grand_central",{"weight": 0.65,"type":"proximity",   "bidirectional": False}),
    ("water_125th",       "transit_125th",       {"weight": 0.75,"type": "proximity",   "bidirectional": False}),
    ("water_brooklyn_atl","transit_atlantic",    {"weight": 0.7, "type": "proximity",   "bidirectional": False}),
    ("water_queens_jax",  "transit_jackson_hts", {"weight": 0.7, "type": "proximity",   "bidirectional": False}),
    ("water_lower_east",  "transit_fulton",      {"weight": 0.6, "type": "proximity",   "bidirectional": False}),

    # ── Cross-domain: water → health (supply dependency) ────────────────────
    ("water_34th",        "health_bellevue",     {"weight": 0.8, "type": "dependency",  "bidirectional": False}),
    ("water_34th",        "health_nyu",          {"weight": 0.8, "type": "dependency",  "bidirectional": False}),
    ("water_42nd",        "health_nyu",          {"weight": 0.7, "type": "dependency",  "bidirectional": False}),
    ("water_uptown",      "health_mount_sinai",  {"weight": 0.75,"type": "dependency",  "bidirectional": False}),
    ("water_125th",       "health_mount_sinai",  {"weight": 0.7, "type": "proximity",   "bidirectional": False}),
    ("water_125th",       "health_presbyterian", {"weight": 0.65,"type": "dependency",  "bidirectional": False}),
    ("water_bronx_hunts", "health_lincoln",      {"weight": 0.75,"type": "dependency",  "bidirectional": False}),
    ("water_brooklyn_hts","health_maimonides",   {"weight": 0.7, "type": "dependency",  "bidirectional": False}),
    ("water_brooklyn_atl","health_kings_county", {"weight": 0.75,"type": "dependency",  "bidirectional": False}),
    ("water_queens_jax",  "health_elmhurst",     {"weight": 0.7, "type": "dependency",  "bidirectional": False}),
    ("water_queens_jax",  "health_jamaica",      {"weight": 0.65,"type": "dependency",  "bidirectional": False}),
    ("water_staten",      "health_maimonides",   {"weight": 0.4, "type": "dependency",  "bidirectional": False}),

    # ── Cross-domain: transit → health (patient transport) ──────────────────
    ("transit_34th_herald","health_bellevue",    {"weight": 0.6, "type": "proximity",   "bidirectional": False}),
    ("transit_34th_herald","health_nyu",         {"weight": 0.6, "type": "proximity",   "bidirectional": False}),
    ("transit_125th",     "health_mount_sinai",  {"weight": 0.6, "type": "proximity",   "bidirectional": False}),
    ("transit_atlantic",  "health_kings_county", {"weight": 0.55,"type": "proximity",   "bidirectional": False}),
    ("transit_jackson_hts","health_elmhurst",    {"weight": 0.6, "type": "proximity",   "bidirectional": False}),

    # ── Cross-domain: emergency → health (EMS delivery) ─────────────────────
    ("emrg_ems_manhattan","health_bellevue",     {"weight": 0.95,"type": "operational", "bidirectional": False}),
    ("emrg_ems_manhattan","health_nyu",          {"weight": 0.9, "type": "operational", "bidirectional": False}),
    ("emrg_fdny_harlem",  "health_mount_sinai",  {"weight": 0.85,"type": "operational", "bidirectional": False}),
    ("emrg_fdny_harlem",  "health_lincoln",      {"weight": 0.8, "type": "operational", "bidirectional": False}),
    ("emrg_fdny_brooklyn","health_kings_county", {"weight": 0.85,"type": "operational", "bidirectional": False}),
    ("emrg_fdny_brooklyn","health_maimonides",   {"weight": 0.7, "type": "operational", "bidirectional": False}),
    ("emrg_fdny_downtown","health_bellevue",     {"weight": 0.8, "type": "operational", "bidirectional": False}),
    ("emrg_fdny_downtown","health_nyu",          {"weight": 0.75,"type": "operational", "bidirectional": False}),
    ("emrg_nypd_harlem",  "health_presbyterian", {"weight": 0.7, "type": "operational", "bidirectional": False}),

    # ── Cross-domain: emergency → transit (rapid response corridors) ─────────
    ("emrg_oem",          "transit_times_sq",    {"weight": 0.6, "type": "operational", "bidirectional": False}),
    ("emrg_oem",          "transit_grand_central",{"weight": 0.6,"type": "operational", "bidirectional": False}),
    ("emrg_nypd_midtown", "transit_times_sq",    {"weight": 0.65,"type": "operational", "bidirectional": False}),
    ("emrg_nypd_midtown", "transit_grand_central",{"weight": 0.6,"type": "operational", "bidirectional": False}),
    ("emrg_fdny_midtown", "transit_times_sq",    {"weight": 0.65,"type": "operational", "bidirectional": False}),
]


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

class InfrastructureGraph:
    def __init__(self) -> None:
        self.G: nx.DiGraph = nx.DiGraph()
        self._build()

    def _build(self) -> None:
        for node in _RAW_NODES:
            self.G.add_node(node["id"], **node)

        for src, dst, attrs in _RAW_EDGES:
            self.G.add_edge(src, dst, **attrs)
            if attrs.get("bidirectional"):
                self.G.add_edge(dst, src, **attrs)

    def get_nodes(self) -> list[dict]:
        result = []
        for node_id, data in self.G.nodes(data=True):
            node = dict(data)
            node["connections"] = list(self.G.successors(node_id))
            result.append(node)
        return result

    def get_edges(self) -> list[dict]:
        seen: set[tuple[str, str]] = set()
        result = []
        for src, dst, data in self.G.edges(data=True):
            key = (min(src, dst), max(src, dst)) if data.get("bidirectional") else (src, dst)
            if key in seen:
                continue
            seen.add(key)
            result.append({"source": src, "target": dst, **data})
        return result


# Module-level singleton — built once at import
graph = InfrastructureGraph()
