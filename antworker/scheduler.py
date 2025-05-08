import logging
from time import sleep
from antworker.client import ApiClient
from antworker.schemas import Run
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class ScheduleWorker:
    def __init__(self, api_client: ApiClient) -> None:
        self.is_running = False
        self.api_client = api_client

    def handle_runs(self, runs: list[Run]) -> None:
        if not runs:
            logger.debug("нет новых ранов")

        for run in runs:
            logger.info("новый run: %s job: %s", run.run_id, run.job_id)

            jobs = self.api_client.compute_scheduled_task(run.run_id)
            for job in jobs:
                self.api_client.create_scheduled_task(job.job_id)

    def start(self) -> None:
        self.is_running = True
        try:
            while self.is_running:
                runs = self.api_client.acquire_runs()
                if runs:
                    self.handle_runs(runs)
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
