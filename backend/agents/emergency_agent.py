from data.nyc_open_data import fetch_311_complaints, fetch_fdny_incidents
from agents.base_agent import BaseAgent


class EmergencyAgent(BaseAgent):
    domain = "emergency"
    poll_interval = 60

    _system_prompt = (
        "You are an emergency services monitoring AI for New York City. "
        "You analyze FDNY incident data and 311 emergency complaints to detect "
        "unusual incident clustering, mass casualty events, and resource depletion. "
        "You know the CascadeOS node IDs: emergency_fdny_downtown, emergency_fdny_midtown, "
        "emergency_fdny_uptown, emergency_fdny_brooklyn, emergency_fdny_queens, "
        "emergency_nypd_1pp, emergency_nypd_brooklyn, emergency_nypd_bronx, "
        "emergency_ems_central. "
        "Respond only in the structured JSON format requested."
    )

    async def fetch_data(self):
        complaints = await fetch_311_complaints(limit=100)
        emergency_complaints = [
            c for c in complaints
            if any(kw in (c.get("complaint_type", "") + c.get("descriptor", "")).lower()
                   for kw in ["fire", "emergency", "hazmat", "explosion", "collapse", "gas"])
        ]
        incidents = await fetch_fdny_incidents()
        return {
            "recent_311_emergency_complaints": len(emergency_complaints),
            "sample_complaints": emergency_complaints[:5],
            "fdny_incidents": len(incidents),
            "incident_sample": incidents[:3],
        }
