from client import ApiClient
from scheduler import Worker


def main():
    api_client = ApiClient()
    worker = Worker(api_client)
    worker.start()


if __name__ == "__main__":
    main()
