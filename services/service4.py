from typing import List
from nameko.rpc import rpc
from nameko.events import event_handler
from nameko.messaging import Publisher
from kombu.messaging import Exchange
from nameko_redis import Redis


class Service4:
    name = 'service4'
    _redis = Redis('my_redis')
    _publication = Exchange('new_publication', type='direct')
    publish = Publisher(exchange=_publication)

    @event_handler('service3', 'number_published')
    def receive_publication(self, payload: str):
        self.dispatch_publication(payload)

    @rpc
    def dispatch_publication(self, payload: str):
        """
        Notify an event with the passed payload

        :param payload: A published number to be notify to the client
        """
        self.publish(payload)

    @rpc
    def get_history(self) -> List[str]:
        if self._redis.llen('published_numbers') > 100:
            history = self._redis.lrange('published_numbers', -100, -1)
        else:
            history = self._redis.lrange('published_numbers', 0, -1)
        return history
