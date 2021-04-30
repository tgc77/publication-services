from nameko.rpc import rpc
from random import randrange


class Service2:
    name = 'service2'

    @rpc
    def request_number(self) -> int:
        return self._generate_odd_number()

    def _generate_odd_number(self) -> int:
        odd_number = randrange(0 + 1, 1000, 2)
        return odd_number
