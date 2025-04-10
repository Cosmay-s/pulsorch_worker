import logging
from time import sleep


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


class ScheduleWorker:
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
