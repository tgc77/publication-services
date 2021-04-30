from nameko.rpc import rpc
from random import randrange


class Service1:
    name = 'service1'

    @rpc
    def request_number(self) -> int:
        return self._generate_even_number()

    def _generate_even_number(self) -> int:
        even_number = randrange(0, 1000, 2)
        return even_number
