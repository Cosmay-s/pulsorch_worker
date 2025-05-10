import httpx
from worker.schemas import Run, ScheduledTask, Job, System
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.Client(base_url=self.base_url)

    def acquire_runs(self) -> list[Run]:
        try:
            logger.debug("запрос runs: %s", self.base_url)
            response = self.client.post("/api/v1/srv/runs/acquire", json={})
            response.raise_for_status()
            data = response.json()
            return [Run(**run) for run in data]
        except Exception:
            logger.exception("не удалось получить runs")
            raise

    def compute_scheduled_task(self, run_id: str) -> list[int]:
        try:
            logger.debug("ищем готовые run: %s", run_id)
            response = self.client.post(f"/api/v1/srv/runs/{run_id}/schedule",
                                        json={})
            response.raise_for_status()
            data = response.json()
            return data.get("job_ids", [])
        except Exception:
            logger.exception("не удалось ")
            raise

    def create_scheduled_task(self, job_id: int) -> ScheduledTask:
        try:
            logger.debug("создать scheduled task")
            response = self.client.post("/api/v1/admin/scheduleds/",
                                        json={"job_id": job_id})
            response.raise_for_status()
            data = response.json()
            return ScheduledTask(**data)
        except Exception:
            logger.exception("не удалось создать scheduled task")
            raise

    def get_scheduled_tasks(self) -> list[ScheduledTask]:
        try:
            api_path = "/api/v1/admin/scheduleds/"
            logger.debug("запрос scheduled tasks: %s", self.base_url)
            response = self.client.get(api_path)
            response.raise_for_status()
            data = response.json()
            return [ScheduledTask(**task) for task in data]
        except Exception:
            logger.exception("не удалось получить scheduled tasks")
            raise

    def get_task_job(self, job_id: int) -> Job:
        api_path = f"/api/v1/admin/jobs/{job_id}"
        response = self.client.get(api_path)
        response.raise_for_status()
        job = response.json()
        return Job(**job)

    def get_task_system(self, system_id: int) -> System:
        api_path = f"/api/v1/admin/systems/{system_id}"
        response = self.client.get(api_path)
        response.raise_for_status()
        system = response.json()
        return System(**system)

    def update_task_status(self, task_id: int):
        api_path = f"/api/v1/admin/scheduleds/{task_id}/triggered"
        response = self.client.post(api_path)
        response.raise_for_status()
        logger.info("Task status update")
        return {}, 204
