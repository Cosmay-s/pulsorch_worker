import httpx
import logging
from time import sleep
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, url):
        self.url = url
        self.client = httpx.Client()

    def get_runs(self):
        try:
            logger.info("Запрос данных с API")
            response = self.client.get(self.url)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            logger.exception("Ошибка при запросе данных")
            return {"error": str(e)}, 500


class Worker:
    def __init__(self, api_client):
        self.is_running = False
        self.seen_runs = set()
        self.api_client = api_client

    def get_new_runs(self, data):
        new_run_found = False
        for run in data:
            run_id = run.get('run_id')
            if run_id and run_id not in self.seen_runs:
                logger.info(f"Новый run: {json.dumps(run, indent=2)}")
                self.seen_runs.add(run_id)
                new_run_found = True
        if not new_run_found:
            logger.info("Нет новых ранов.")

    def start(self):
        self.is_running = True
        while self.is_running:
            data = self.api_client.get_runs()
            if data:
                self.get_new_runs(data)
            sleep(30)


def main():
    url = "http://localhost:8080/api/v1/srv/runs/?after=2025-03-25T14:50:00.000000+00:00&orderby=updated_at"
    api_client = ApiClient(url)
    worker = Worker(api_client)
    worker.start()


if __name__ == "__main__":
    main()
