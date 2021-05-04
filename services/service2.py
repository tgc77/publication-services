from nameko.rpc import rpc
from random import randrange


class Service2:
    """
    Microservice responsible for generate random odd numbers and listening for
    requests from another microservices that implements RpcProxy connector.

    Attributes:
        name (str): The microservice name
    """

    name = 'service2'

    @rpc
    def request_number(self) -> int:
        """
        Listener function called from microservices which have implemented
        a RpcProxy connector.

        Returns:
            int: Delegated funtion result.
        """
        return self._generate_odd_number()

    def _generate_odd_number(self) -> int:
        """
        Generates odd random numbers

        Returns:
            int: Odd number generated
        """
        odd_number = randrange(0 + 1, 1000, 2)
        return odd_number
