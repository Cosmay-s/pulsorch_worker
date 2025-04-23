import logging
from time import sleep
from client import ApiClient
from schemas import ScheduledTask
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class TriggerWorker:
    def __init__(self, api_client: ApiClient) -> None:
        self.is_running = False
        self.seen_scheduled: set[int] = set()
        self.api_client = api_client

    def get_new_scheduled_tasks(self, tasks: list[ScheduledTask]) -> None:
        new_task_found = False
        for task in tasks:
            if task.scheduled_id not in self.seen_scheduled:
                logger.info(f"Новый task:\n{task}")
                self.seen_scheduled.add(task.scheduled_id)
                new_task_found = True
            if not new_task_found:
                logger.info("Нет новых tasks.")

    def start(self) -> None:
        self.is_running = True
        while self.is_running:
            tasks = self.api_client.get_scheduled_tasks()
            if tasks:
                self.get_new_scheduled_tasks(tasks)
            sleep(15)


def main() -> None:
    logging.info("Starting worker...")
    base_url = os.getenv("BASE_URL")
    api_client = ApiClient(base_url)
    triggerier = TriggerWorker(api_client)
    triggerier.start()
    logging.info("Worker has stopped.")


if __name__ == "__main__":
    main()
