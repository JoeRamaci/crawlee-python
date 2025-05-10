from apify_client.clients import KeyValueStoreClient


class KeyValue(KeyValueStoreClient):
    def __init__(self) -> None:
        super().__init__()
