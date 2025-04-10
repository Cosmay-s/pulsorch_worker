from antworker.client import ApiClient
from antworker.scheduler import ScheduleWorker
import logging
import os
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
load_dotenv()


def main() -> None:
    logging.info("Starting worker...")
    base_url: str = os.getenv("BASE_URL")
    api_client = ApiClient(base_url)
    worker = ScheduleWorker(api_client)
    worker.start()
    logging.info("Worker has stopped.")


if __name__ == "__main__":
    main()
