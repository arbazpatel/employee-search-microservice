from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class OrgConfig(BaseModel):
    name: str
    api_key: str
    display_columns: List[str]
    rate_limit_requests: int = Field(default=100, description="Number of requests allowed")
    rate_limit_seconds: int = Field(default=60, description="Time window in seconds")

ORGANIZATION_CONFIGS: Dict[str, OrgConfig] = {
    "api-key-stark-industries": OrgConfig(
        name="Stark Industries",
        api_key="api-key-stark-industries",
        display_columns=["email", "department", "position", "location", "employee_ssn"],
        rate_limit_requests=50,
        rate_limit_seconds=60,
    ),
    "api-key-wayne-enterprises": OrgConfig(
        name="Wayne Enterprises",
        api_key="api-key-wayne-enterprises",
        display_columns=["first_name", "last_name", "location"],
        rate_limit_requests=5,
        rate_limit_seconds=10,
    ),
}

def get_org_config_by_key(api_key: str) -> Optional[OrgConfig]:
    return ORGANIZATION_CONFIGS.get(api_key)