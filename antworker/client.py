import httpx
from datetime import datetime, timedelta
from schemas import Run, ScheduledTask, Job, System
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

    def get_runs(self, after_date: datetime = None) -> list[Run]:
        try:
            api_path = "/api/v1/srv/runs/"
            after_date = after_date or datetime.now() - timedelta(days=1)
            after_date_str = after_date.isoformat()
            params = {
                'after': after_date_str,
                'orderby': 'updated_at'
            }
            logger.info(f"Запрос данных: {self.base_url}")
            response = self.client.get(api_path, params=params)
            response.raise_for_status()
            data = response.json()
            return [Run(**run) for run in data]
        except Exception as e:
            logger.exception("Ошибка при запросе данных")
            return {"error": str(e)}, 500

    def get_scheduled_tasks(self) -> list[ScheduledTask]:
        try:
            api_path = "/api/v1/admin/scheduleds/"
            logger.info(f"Запрос данных: {self.base_url}")
            response = self.client.get(api_path)
            response.raise_for_status()
            data = response.json()
            return [ScheduledTask(**task) for task in data]
        except Exception as e:
            logger.exception("Ошибка при запросе данных")
            return {"error": str(e)}, 500

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
