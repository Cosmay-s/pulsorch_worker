from pydantic import BaseModel
from enum import Enum as PyEnum


class RunStatus(PyEnum):
    created = "created"
    scheduled = "scheduled"
    triggered = "triggered"


class Run(BaseModel):
    run_id: str
    job_id: int
    external_status: str
    start_time: str
    created_at: str | None
    updated_at: str | None
    status: RunStatus
