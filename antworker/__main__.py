# from antworker.client import ApiClient
# from antworker.scheduler import ScheduleWorker
# from antworker.triggerier import TriggerWorker
# import logging
# import os
# from dotenv import load_dotenv


# logger = logging.getLogger(__name__)
# load_dotenv()


# def main() -> None:
#     logging.info("Starting worker...")
#     base_url = os.getenv("BASE_URL")
#     api_client = ApiClient(base_url)
#     scheduler = ScheduleWorker(api_client)
#     triggerier = TriggerWorker(api_client) 
#     scheduler.start()
#     triggerier.start()
#     logging.info("Worker has stopped.")


# if __name__ == "__main__":
#     main()
