from pydantic import BaseModel
import enum


class RunStatus(enum.Enum):
    CREATED = "created"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"


class ScheduledStatus(enum.Enum):
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"
    CANCELLED = "cancelled"


class Run(BaseModel):
    run_id: str
    job_id: int
    external_status: str
    start_time: str
    created_at: str | None
    updated_at: str | None
    status: RunStatus


class ScheduledTask(BaseModel):
    scheduled_id: int
    job_id: int
    scheduled_at: str
    status: ScheduledStatus
