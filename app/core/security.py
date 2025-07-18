from fastapi import Request, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS
from time import time
from typing import Dict, List

from app.core.config import OrgConfig, get_org_config_by_key

REQUEST_LOGS: Dict[str, List[float]] = {}

def get_current_org(request: Request) -> OrgConfig:
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is missing or invalid",
        )

    org_config = get_org_config_by_key(api_key)
    if not org_config:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is missing or invalid",
        )

    now = time()
    time_window = org_config.rate_limit_seconds
    max_requests = org_config.rate_limit_requests

    request_timestamps = REQUEST_LOGS.get(api_key, [])

    relevant_timestamps = [timestamp for timestamp in request_timestamps if now - timestamp < time_window]

    if len(relevant_timestamps) >= max_requests:
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Too Many Requests",
        )
    relevant_timestamps.append(now)
    REQUEST_LOGS[api_key] = relevant_timestamps

    return org_config