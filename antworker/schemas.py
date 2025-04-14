from pydantic import BaseModel


class Run(BaseModel):
    run_id: str
    job_id: int
    external_status: str
    start_time: str
    created_at: str | None
    updated_at: str | None
