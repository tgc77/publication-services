from functools import reduce
from nameko.testing.utils import get_container
from nameko.testing.services import (
    entrypoint_hook,
    worker_factory
)

from services.service3 import Service3
from services.service2 import Service2
from services.service1 import Service1


def test_request_numbers():
    service3 = worker_factory(Service3)

    # Add side effects to the mock proxy dependecies services
    service3._service1.request_number.side_effect = lambda: 777
    service3._service2.request_number.side_effect = lambda: 999

    # Test request_number business logic from service1 and service2
    even_number = service3._service1.request_number()
    assert even_number == 777

    odd_number = service3._service2.request_number()
    assert odd_number == 999

    # Mock redis attribute to storage publications
    setattr(service3._redis, 'published_numbers', list())

    # Mock redis rpush method
    def rpush_mock(key, value):
        mlist = getattr(service3._redis, key)
        mlist.append(value)

    service3._redis.rpush.side_effect = rpush_mock

    # Mock service apply_rule method to publish result if applying rule matchs
    def apply_rule_mock(numbers):
        result = reduce(lambda n1, n2: n1 * n2, numbers)
        if result > 100000:
            service3._redis.rpush('published_numbers', str(result))
        return result

    service3._apply_rule = apply_rule_mock
    result = service3._apply_rule((even_number, odd_number))
    assert result == 776223

    # Mock redis lrange method to get published publications
    def lrange_mock(key, start, end):
        mlist = getattr(service3._redis, key)
        return mlist[start:end]

    service3._redis.lrange.side_effect = lrange_mock
    published_number = service3._redis.lrange('published_numbers', 0, 1)
    assert published_number[0] == str(776223)

    # Dispatch notification of new publication
    assert service3.notify_publication(payload=str(result)) == None


def test_service_integration(runner_factory, rabbit_config):
    config = rabbit_config
    config['REDIS_URIS'] = {'my_redis': 'redis://localhost:6379/0'}
    runner = runner_factory(rabbit_config, Service1, Service2, Service3)

    service3 = get_container(runner, Service3)

    runner.start()

    with entrypoint_hook(service3, 'request_numbers') as request_numbers:
        request_numbers()
