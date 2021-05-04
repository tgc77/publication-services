
class ClientConsumer:
    """
    Client Consumer to manage getting and displaying incoming publications.

    Attributes:
       _publications_counter (int) : static publications counter
       _redis_client (FlaskRedis) : Redis client connector
    """

    _publications_counter: int = 0

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    @property
    def max_size(self):
        return self._max_size

    def init_app(self, redis_client):
        self._redis_client = redis_client

    def publications_count(self):
        return self._publications_counter

    def check_counter(self):
        if self._publications_counter > self.max_size:
            self._publications_counter = 0
        self._publications_counter += 1

    def consume_publication(self):
        try:
            publication = self._redis_client.lpop('publication_queue')
            if publication is not None:
                self.check_counter()
            return publication
        except Exception as e:
            print('Ooops!', e)
            return None
