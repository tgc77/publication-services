from services.service1 import Service1
from nameko.testing.services import worker_factory


def test_request_number():
    service1 = worker_factory(Service1)
    result = service1.request_number()
    assert result % 2 == 0


# def test_service_integration(runner_factory, rabbit_config):
#     service1 = runner_factory(Service1, rabbit_config)
#     service1.start()
