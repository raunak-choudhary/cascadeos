from data.nyc_open_data import fetch_311_complaints, fetch_hospital_capacity
from agents.base_agent import BaseAgent


class HealthAgent(BaseAgent):
    domain = "health"
    poll_interval = 90

    _system_prompt = (
        "You are a health infrastructure monitoring AI for New York City. "
        "You analyze hospital capacity data and 311 health-related complaints to detect "
        "ER overcapacity, ambulance availability drops, and public health surges. "
        "You know the CascadeOS node IDs: health_bellevue, health_nyu_langone, "
        "health_mount_sinai, health_nypres, health_kings_county, health_maimonides, "
        "health_jamaica, health_lincoln, health_harlem. "
        "Respond only in the structured JSON format requested."
    )

    async def fetch_data(self):
        complaints = await fetch_311_complaints(limit=100)
        health_complaints = [
            c for c in complaints
            if any(kw in (c.get("complaint_type", "") + c.get("descriptor", "")).lower()
                   for kw in ["health", "hospital", "ambulance", "medical", "overdose"])
        ]
        capacity = await fetch_hospital_capacity()
        return {
            "recent_311_health_complaints": len(health_complaints),
            "sample_complaints": health_complaints[:5],
            "hospital_capacity_records": len(capacity),
            "capacity_sample": capacity[:3],
        }
