# cache_manager.py
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any

CACHE_FILE = Path("cache.json")
DEFAULT_MAX_AGE_MINUTES = 10  # default freshness window

def _read_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _write_cache(data: dict):
    CACHE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def save(key: str, data: Any):
    cache = _read_cache()
    cache[key] = {
        "ts": datetime.utcnow().isoformat(),
        "data": data
    }
    _write_cache(cache)

def load(key: str, max_age_minutes: int = DEFAULT_MAX_AGE_MINUTES) -> Optional[Any]:
    cache = _read_cache()
    rec = cache.get(key)
    if not rec:
        return None
    try:
        ts = datetime.fromisoformat(rec["ts"])
    except Exception:
        return None
    if datetime.utcnow() - ts > timedelta(minutes=max_age_minutes):
        return None
    return rec["data"]

def clear():
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
