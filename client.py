import httpx
from datetime import datetime, timedelta
from schemas import Run
import logging


logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client()

    def get_runs(self, after_date: datetime = None) -> list[Run]:
        try:
            after_date = after_date or datetime.now() - timedelta(days=1)
            after_date_str = after_date.isoformat()
            params = {
                'after': after_date_str,
                'orderby': 'updated_at'
            }
            logger.info(f"Запрос данных с API: {self.base_url}")
            response = self.client.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()
            runs = [
                Run(
                    run_id=data_run['run_id'],
                    job_id=data_run['job_id'],
                    status=data_run['status'],
                    start_time=data_run['start_time'],
                    created_at=data_run['created_at'],
                    updated_at=data_run['updated_at']
                )
                for data_run in data
            ]
            return runs
        except Exception as e:
            logger.exception("Ошибка при запросе данных с API")
            return {"error": str(e)}, 500
