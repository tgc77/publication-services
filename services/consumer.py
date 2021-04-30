from nameko.messaging import consume
from kombu.messaging import Exchange, Queue
from nameko_redis import Redis


class ConsumerService:
    name = 'consumer'
    _publication = Exchange('new_publication', type='direct')
    _queue = Queue('publication_queue', exchange=_publication)
    _redis = Redis('my_redis')

    @consume(_queue)
    def receive_new_publication(self, payload):
        try:
            self._redis.rpush('publication_queue', payload)
        except Exception as e:
            print('Ooops!', e)
