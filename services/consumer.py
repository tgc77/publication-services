from nameko.messaging import consume
from kombu.messaging import Exchange, Queue
from nameko_redis import Redis


class ConsumerService:
    """
    Microservice responsible for consume data notifications from Service4 and
    dispatching those data to the Client by saving those data to Redis database.

    Attributes:
        name (str): The microservice name.
        _publication (Exchange): Messagin exchange object.
        _queue  (Queue): Messaging publications queue to be consumed.
        _redis (Redis): Nameko Redis connector object.
    """

    name = 'consumer'
    _publication = Exchange('new_publication', type='direct')
    _queue = Queue('publication_queue', exchange=_publication)
    _redis = Redis('my_redis')

    @consume(_queue)
    def receive_new_publication(self, payload: str):
        """
        Responsible for consuming incoming data received from service4 by
        saving data to Redis Queue.

        Args:
            payload (str): Data to be consumed.
        """
        try:
            self._redis.rpush('publication_queue', payload)
        except Exception as e:
            print('Ooops!', e)
