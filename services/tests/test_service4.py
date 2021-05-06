from nameko.testing.utils import get_container
from nameko.standalone.events import event_dispatcher
from nameko.testing.services import (
    entrypoint_hook, entrypoint_waiter, worker_factory
)
from mock import patch
from random import sample

from services.service4 import Service4
from services.service3 import Service3
from services.service2 import Service2
from services.service1 import Service1

MY_REDIS_URIS = {'my_redis': 'redis://localhost:6379/0'}
#
################### Unit Tests ###################
#


@patch('nameko.testing.services.entrypoint_waiter')
@patch('nameko.standalone.events.event_dispatcher')
def test_receive_publication(event_dispatcher_mock, entrypoint_waiter_mock):
    service4 = worker_factory(Service4)

    event_dispatcher_mock.return_value = lambda s, ev, val: val

    payload = '776223'
    dispatch = event_dispatcher_mock()
    with entrypoint_waiter_mock(service4, 'receive_publication'):
        assert dispatch('service3', 'number_published', payload) == payload


def test_get_history():
    service4 = worker_factory(Service4)

    # Mock redis attribute to storage publications
    mlist = sample(range(100000, 999999), 100)
    setattr(service4._redis, 'published_numbers', mlist)

    # Mock redis llen method
    def llen_mock(key):
        mlist = getattr(service4._redis, key)
        return len(mlist)
    service4._redis.llen.side_effect = llen_mock

    # Mock redis lrange method to get published publications
    def lrange_mock(key, start, end):
        mlist = getattr(service4._redis, key)
        if end == -1:
            return mlist[start:]
        return mlist[start:end]
    service4._redis.lrange.side_effect = lrange_mock
    history = service4._redis.lrange('published_numbers', 0, -1)
    mlistlen = service4._redis.llen('published_numbers')
    assert mlistlen == len(history)
    assert isinstance(history, list)

#
################### Integration Tests ###################
#


def test_service_integration(container_factory, rabbit_config):
    config = rabbit_config
    config['REDIS_URIS'] = MY_REDIS_URIS
    service4 = container_factory(Service4, config)
    service4.start()

    payload = '776223'
    dispatch = event_dispatcher(rabbit_config)
    with entrypoint_waiter(service4, 'receive_publication'):
        dispatch('service3', 'number_published', payload)


def test_request_numbers_integration(runner_factory, rabbit_config):
    config = rabbit_config
    config['REDIS_URIS'] = MY_REDIS_URIS
    runner = runner_factory(config, Service1,
                            Service2, Service3, Service4)
    runner.start()

    service3 = get_container(runner, Service3)
    service4 = get_container(runner, Service4)
    with entrypoint_hook(service3, 'request_numbers') as request_numbers:
        with entrypoint_waiter(service4, 'receive_publication'):
            request_numbers()


def test_get_history_integration(container_factory, rabbit_config):
    config = rabbit_config
    config['REDIS_URIS'] = MY_REDIS_URIS
    service4 = container_factory(Service4, config)
    service4.start()

    with entrypoint_hook(service4, 'get_history') as get_history:
        result = get_history()
    assert isinstance(result, list)
