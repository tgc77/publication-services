from nameko.rpc import rpc
from random import randrange


class Service1:
    """
    Microservice responsible for generate even random numbers and listening for
    requests from another microservices that implements RpcProxy connector.

    Attributes:
        name (str): The microservice name
    """

    name = 'service1'

    @rpc
    def request_number(self) -> int:
        """
        Listener function called from microservices which have implemented
        a RpcProxy connector.

        Returns:
            int: Delegated funtion result.
        """
        return self._generate_even_number()

    def _generate_even_number(self) -> int:
        """
        Generates even random numbers

        Returns:
            int: Even number generated
        """
        even_number = randrange(0, 1000, 2)
        return even_number
