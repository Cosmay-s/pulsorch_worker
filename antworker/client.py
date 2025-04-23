import httpx
from datetime import datetime, timedelta
from antworker.schemas import Run, ScheduledTask
import logging


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
            runs = []
            for data_run in data:
                runs.append(Run(**data_run))
            return runs
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
            scheduled_tasks = []
            for task in data:
                scheduled_tasks.append(ScheduledTask(**task))
            return scheduled_tasks
        except Exception as e:
            logger.exception("Ошибка при запросе данных")
            return {"error": str(e)}, 500
