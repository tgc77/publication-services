from typing import List
from nameko.rpc import rpc
from nameko.events import event_handler
from nameko.messaging import Publisher
from kombu.messaging import Exchange
from nameko_redis import Redis


class Service4:
    """
    Microservice responsible for receiving data notifications from Service3 and
    dispatching those data to the Client.

    Attributes:
        name (str): The microservice name.
        _redis (Redis): Nameko Redis connector object.
        _publication (Exchange): Messagin exchange object.
        _publish  (Publisher): Messaging publisher object.
    """

    name = 'service4'
    _redis = Redis('my_redis')
    _publication = Exchange('new_publication', type='direct')
    _publish = Publisher(exchange=_publication)

    @event_handler('service3', 'number_published')
    def receive_publication(self, payload: str):
        """
        Event handler function receiver published number from service3

        Args:
            payload (str): A new number published according service3 rules
        """
        self.dispatch_publication(payload)

    @rpc
    def dispatch_publication(self, payload: str):
        """
        Notify an event with the passed payload

        :param payload: A published number to be notify to the client
        """
        self._publish(payload)

    @rpc
    def get_history(self) -> List[str]:
        """
        Get the last 100 publications from Redis Database

        Returns:
            List[str]: Last publications
        """
        if self._redis.llen('published_numbers') > 100:
            history = self._redis.lrange('published_numbers', -100, -1)
        else:
            history = self._redis.lrange('published_numbers', 0, -1)
        return history
