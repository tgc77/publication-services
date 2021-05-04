from services.service2 import Service2
from nameko.testing.services import worker_factory


def test_request_number():
    service2 = worker_factory(Service2)
    result = service2.request_number()
    assert result % 2 == 1
