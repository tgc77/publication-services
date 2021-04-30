from functools import reduce
from typing import Tuple
from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
from nameko.events import EventDispatcher
from nameko_redis import Redis


class Service3:
    name = 'service3'
    _service1 = RpcProxy('service1')
    _service2 = RpcProxy('service2')
    _dispatch = EventDispatcher()
    _redis = Redis('my_redis')

    @rpc
    def notify_publication(self, payload: str):
        """
        Notify an event with the passed payload

        :param payload: A published number to be notify to the api-gateway
        """
        self._dispatch('number_published', payload)

    @timer(interval=0.5)
    @rpc
    def request_numbers(self):
        even_number = -1
        odd_number = -1
        try:
            even_number = self._service1.request_number()
            odd_number = self._service2.request_number()
            self._apply_rule((even_number, odd_number))
        except Exception as e:
            print('Ooopss!', e)

    def _apply_rule(self, numbers: Tuple[int, int]) -> None:
        result = reduce(lambda n1, n2: n1 * n2, numbers)
        if result > 100000:
            self._publish_result(str(result))

    def _publish_result(self, result: str) -> None:
        try:
            self._redis.lpush('published_numbers', result)
            self.notify_publication(result)
        except Exception as e:
            print('Oopps!', e)
