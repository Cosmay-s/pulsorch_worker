from pydantic import BaseModel


class Run(BaseModel):
    run_id: str
    job_id: int
    status: str
    start_time: str
    created_at: str | None
    updated_at: str | None


# @dc.dataclass
# class System:
#     system_id: int
#     code: str
#     url: str
#     token: str
#     system_type: str
#     created_at: datetime | None
#     updated_at: datetime | None


# @dc.dataclass
# class Job:
#     job_id: int
#     system_id: int
#     code: str
#     scheduler: str
#     created_at: datetime | None
#     updated_at: datetime | None


# @dc.dataclass
# class Dependence:
#     dependence_id: int
#     completed_job_id: int
#     trigger_job_id: int
#     # parent_scheduler: str
#     created_at: datetime | None
#     updated_at: datetime | None
