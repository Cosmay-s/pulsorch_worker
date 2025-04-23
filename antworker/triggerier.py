import logging
from time import sleep
from antworker.client import ApiClient
from antworker.schemas import ScheduledTask


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


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
