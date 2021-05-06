import unittest2

from client.app import create_app
from client.app.config import Config


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'khebiqw4o314h32ghf3fgh3gfy138bfy8vfyvf3fvy8f'
    SERVICE_CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost:5672/"}
    SERVICE_PROVIDER = "service4"
    REDIS_URL = "redis://localhost:6379/0"


class BaseTestCase(unittest2.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.test_rctx = self.app.test_request_context()
        self.adapter = self.app.url_map.bind('')

    def tearDown(self):
        self.app_context.pop()
