from functools import reduce
from typing import Tuple
from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
from nameko.events import EventDispatcher
from nameko_redis import Redis


class Service3:
    """
    Microservice responsible for request data from Service1 and Service2 and
    dispatching those data notification to another microservice which implements
    an @event_handler listener.

    Attributes:
        name (str): The microservice name
        _service1 (RpcProxy): Nameko RpcProxy connector to another microservice.
        _service2 (RpcProxy): Nameko RpcProxy connector to another microservice.
        _dispatch  (EventDispatcher): Messaging event dispatcher object.
        _redis (Redis): Nameko Redis connector object.
    """

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

    @rpc
    @timer(interval=0.5)
    def request_numbers(self):
        """
        Requests numbers each 500ms interval from service1 and service2 and
        apply some rule to be processed.
        """
        # Initialize parameters to be able to use into try block.
        even_number = -1
        odd_number = -1
        try:
            even_number = self._service1.request_number()
            odd_number = self._service2.request_number()
            self._apply_rule((even_number, odd_number))
        except Exception as e:
            print('Ooopss!', e)

    def _apply_rule(self, numbers: Tuple[int, int]):
        """
        Function responsible for applying some processing rule to the requested
        numbers and call self._publish_result if the rule matchs.

        Args:
            numbers (Tuple[int, int]): Requested numbers from service1 and service2
        """
        result = reduce(lambda n1, n2: n1 * n2, numbers)
        if result > 100000:
            self._publish_result(str(result))

    def _publish_result(self, result: str):
        """
        Publish the result to Redis database for future history and notify the
        action to listening consumers.

        Args:
            result (str): Result from data rule applyied.
        """
        try:
            self._redis.rpush('published_numbers', result)
            self.notify_publication(result)
        except Exception as e:
            print('Oopps!', e)
