from . import redis_client


class ClientConsumer:
    _publications_counter = 0

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    @property
    def max_size(self):
        return self._max_size

    def publications_count(self):
        return self._publications_counter

    def check_counter(self):
        if self._publications_counter > self._max_size:
            self._publications_counter = 0
        self._publications_counter += 1

    def consume_publication(self):
        try:
            publication = redis_client.lpop('publication_queue')
            if publication is not None:
                self.check_counter()
            return publication
        except Exception as e:
            print('Ooops!', e)
            return None
