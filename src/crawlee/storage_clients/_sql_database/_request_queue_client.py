from apify_client.clients import RequestQueueClient


class RequestQueue(RequestQueueClient):
    def __init__(self) -> None:
        super().__init__()
