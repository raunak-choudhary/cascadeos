from data.nyc_open_data import fetch_311_complaints, fetch_water_main_data
from agents.base_agent import BaseAgent


class WaterAgent(BaseAgent):
    domain = "water"
    poll_interval = 60

    _system_prompt = (
        "You are a water infrastructure monitoring AI for New York City. "
        "You analyze NYC DEP water main data and 311 water complaints to detect "
        "pressure anomalies, main breaks, and flooding risks. "
        "You know the CascadeOS node IDs: water_34th, water_herald_sq, water_brooklyn_main, "
        "water_queens_pump, water_manhattan_bridge, water_bronx_hub, water_staten_island, "
        "water_williamsburg, water_astoria, water_upper_manhattan. "
        "Respond only in the structured JSON format requested."
    )

    async def fetch_data(self):
        complaints = await fetch_311_complaints(limit=100)
        water_complaints = [
            c for c in complaints
            if "water" in (c.get("complaint_type", "") + c.get("descriptor", "")).lower()
        ]
        main_breaks = await fetch_water_main_data()
        return {
            "recent_311_water_complaints": len(water_complaints),
            "sample_complaints": water_complaints[:5],
            "active_main_breaks": len(main_breaks),
            "break_sample": main_breaks[:3],
        }
