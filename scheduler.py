from time import sleep
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


logger = logging.getLogger(__name__)


class Worker:
    def __init__(self):
        self.is_running = False

    def start(self):
        self.is_running = True
        while self.is_running:
            logger.info("Я работаю.")
            sleep(10)


def main():
    loop = Worker()
    loop.start()


if __name__ == "__main__":
    main()