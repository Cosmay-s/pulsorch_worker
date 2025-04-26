import logging
from time import sleep
from client import ApiClient
from schemas import Run
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class ScheduleWorker:
    def __init__(self, api_client: ApiClient) -> None:
        self.is_running = False
        self.seen_runs: set[int] = set()
        self.api_client = api_client

    def get_new_runs(self, runs: list[Run]) -> None:
        new_run_found = False
        for run in runs:
            if run.run_id not in self.seen_runs:
                logger.info(f"Новый run:\n{run}")
                self.seen_runs.add(run.run_id)
                new_run_found = True
        if not new_run_found:
            logger.info("Нет новых ранов.")

    def start(self) -> None:
        self.is_running = True
        try:
            while self.is_running:
                runs = self.api_client.get_runs()
                if runs:
                    self.get_new_runs(runs)
                sleep(15)
        except KeyboardInterrupt:
            logger.info("Шедулер остановлен")


def main() -> None:
    logging.info("Starting worker...")
    base_url = os.getenv("BASE_URL")
    api_client = ApiClient(base_url)
    scheduler = ScheduleWorker(api_client)
    scheduler.start()
    logging.info("Worker has stopped.")


if __name__ == "__main__":
    main()
