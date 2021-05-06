from nameko.testing.utils import get_container
from nameko.testing.services import (
    entrypoint_hook, entrypoint_waiter, worker_factory
)
from mock import patch

from services.consumer import ConsumerService
from services.service4 import Service4
from services.service3 import Service3
from services.service2 import Service2
from services.service1 import Service1

#
################### Unit Tests ###################
#


@patch('nameko.testing.services.entrypoint_hook')
@patch('nameko.testing.services.entrypoint_waiter')
def test_receive_new_publication(entrypoint_waiter_mock, entrypoint_hook_mock):
    service4 = worker_factory(Service4)
    consumer = worker_factory(ConsumerService)

    payload = '776223'
    with entrypoint_hook_mock(service4, 'dispatch_publication') as dispatch:
        with entrypoint_waiter_mock(consumer, 'receive_new_publication'):
            dispatch(payload)

#
################### Integration Tests ###################
#


def test_consumer_integration(runner_factory, rabbit_config):
    config = rabbit_config
    config['REDIS_URIS'] = {'my_redis': 'redis://localhost:6379/0'}
    runner = runner_factory(config, Service1,
                            Service2, Service3, Service4, ConsumerService)
    runner.start()

    service3 = get_container(runner, Service3)
    consumer = get_container(runner, ConsumerService)
    with entrypoint_hook(service3, 'request_numbers') as request_numbers:
        with entrypoint_waiter(consumer, 'receive_new_publication'):
            request_numbers()
