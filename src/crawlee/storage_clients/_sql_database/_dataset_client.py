from apify_client.clients import DatasetClient


class Dataset(DatasetClient):
    def __init__(self) -> None:
        super().__init__()
