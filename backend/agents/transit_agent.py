from data.nyc_open_data import fetch_311_complaints, fetch_mta_status
from agents.base_agent import BaseAgent


class TransitAgent(BaseAgent):
    domain = "transit"
    poll_interval = 45

    _system_prompt = (
        "You are a transit infrastructure monitoring AI for New York City. "
        "You analyze MTA service status and 311 transit complaints to detect "
        "service disruptions, signal failures, and unusual crowding. "
        "You know the CascadeOS node IDs: transit_times_sq, transit_grand_central, "
        "transit_penn_station, transit_union_sq, transit_34th_herald, transit_atlantic_av, "
        "transit_borough_hall, transit_125th, transit_14th, transit_jackson_hts, "
        "transit_jamaica, transit_fulton. "
        "Respond only in the structured JSON format requested."
    )

    async def fetch_data(self):
        complaints = await fetch_311_complaints(limit=100)
        transit_complaints = [
            c for c in complaints
            if any(kw in (c.get("complaint_type", "") + c.get("descriptor", "")).lower()
                   for kw in ["subway", "train", "mta", "bus", "transit"])
        ]
        mta_status = await fetch_mta_status()
        return {
            "recent_311_transit_complaints": len(transit_complaints),
            "sample_complaints": transit_complaints[:5],
            "mta_alerts": mta_status[:5] if mta_status else [],
        }
