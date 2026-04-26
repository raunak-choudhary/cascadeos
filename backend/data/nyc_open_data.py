"""
NYC Open Data API client.
All requests include the app token from settings.
Rate limit: 1000 req/hour on free tier — poll conservatively.
"""
import httpx
from config import settings

_HEADERS = {"X-App-Token": settings.NYC_OPEN_DATA_APP_TOKEN}
_TIMEOUT = 15.0


async def fetch_311_complaints(limit: int = 200) -> list[dict]:
    """Fetch recent 311 complaints, sorted by created_date descending."""
    params = {
        "$limit": limit,
        "$order": "created_date DESC",
        "$where": "created_date > '2024-01-01T00:00:00.000'",
    }
    async with httpx.AsyncClient(headers=_HEADERS, timeout=_TIMEOUT) as client:
        resp = await client.get(settings.NYC_311_ENDPOINT, params=params)
        resp.raise_for_status()
        return resp.json()


async def fetch_mta_status() -> list[dict]:
    """MTA subway service status — public GTFS-RT / Siri endpoint."""
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
    # MTA real-time feeds are protobuf; fall back to status API for human-readable data
    status_url = "https://collector-otp-prod.camsys-apps.com/realtime/serviceStatus"
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.get(status_url)
            resp.raise_for_status()
            return resp.json() if isinstance(resp.json(), list) else []
    except Exception:
        return []


async def fetch_water_main_data() -> list[dict]:
    """NYC DEP water main break reports from Open Data."""
    url = "https://data.cityofnewyork.us/resource/bdjm-n7q4.json"
    params = {"$limit": 100, "$order": "open_date DESC"}
    try:
        async with httpx.AsyncClient(headers=_HEADERS, timeout=_TIMEOUT) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return []


async def fetch_hospital_capacity() -> list[dict]:
    """NYC Health hospital diversion / capacity data."""
    url = "https://data.cityofnewyork.us/resource/5uac-w243.json"
    params = {"$limit": 50, "$order": "date DESC"}
    try:
        async with httpx.AsyncClient(headers=_HEADERS, timeout=_TIMEOUT) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return []


async def fetch_fdny_incidents() -> list[dict]:
    """FDNY incident dispatch data."""
    url = "https://data.cityofnewyork.us/resource/8m42-w767.json"
    params = {"$limit": 100, "$order": "starfire_incident_datetime DESC"}
    try:
        async with httpx.AsyncClient(headers=_HEADERS, timeout=_TIMEOUT) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return []
