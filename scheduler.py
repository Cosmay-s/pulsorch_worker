import httpx
import logging
from time import sleep
from datetime import datetime, timedelta
import dataclasses as dc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


@dc.dataclass
class Run:
    run_id: str
    job_id: int
    status: str
    start_time: str
    created_at: str | None
    updated_at: str | None

    def __repr__(self):
        return (f"Run(\n"
                f"  run_id={self.run_id},\n"
                f"  job_id={self.job_id},\n"
                f"  status={self.status},\n"
                f"  start_time={self.start_time},\n"
                f"  created_at={self.created_at},\n"
                f"  updated_at={self.updated_at}\n"
                f")")


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.Client()

    def get_runs(self, after_date: datetime = None):
        try:
            after_date = after_date or datetime.now() - timedelta(days=1)
            after_date_str = after_date.isoformat()
            url = f"{self.base_url}?after={after_date_str}&orderby=updated_at"
            logger.info(f"Запрос данных с API: {url}")
            response = self.client.get(url)
            response.raise_for_status()
            data = response.json()
            runs = [Run(
                run_id=data_run['run_id'],
                job_id=data_run['job_id'],
                status=data_run['status'],
                start_time=data_run['start_time'],
                created_at=data_run['created_at'],
                updated_at=data_run['updated_at']
            ) for data_run in data]
            return runs
        except Exception as e:
            logger.exception("Ошибка при запросе данных с API")
            return {"error": str(e)}, 500


class Worker:
    def __init__(self, api_client):
        self.is_running = False
        self.seen_runs = set()
        self.api_client = api_client

    def get_new_runs(self, runs):
        new_run_found = False
        for run in runs:
            if run.run_id not in self.seen_runs:
                logger.info(f"Новый run:\n{run}")
                self.seen_runs.add(run.run_id)
                new_run_found = True
        if not new_run_found:
            logger.info("Нет новых ранов.")

    def start(self):
        self.is_running = True
        while self.is_running:
            runs = self.api_client.get_runs()
            if runs:
                self.get_new_runs(runs)
            sleep(30)


def main():
    base_url = "http://localhost:8080/api/v1/srv/runs/"
    api_client = ApiClient(base_url)
    worker = Worker(api_client)
    worker.start()


if __name__ == "__main__":
    main()
