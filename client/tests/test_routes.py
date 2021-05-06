from werkzeug.exceptions import NotFound
from mock import patch

from client.tests.base_test_case import BaseTestCase


class TestRoutes(BaseTestCase):
    def test_index_page_should_exists(self):
        res = self.client.get('/index', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_wrong_index_page_should_raises_not_found_exception(self):
        with self.assertRaises(NotFound):
            self.adapter.match('/wrong_index')

    def test_get_history(self):
        res = self.client.get('/history')
        self.assertEqual(res.status_code, 200)

    @patch('flask_socketio.emit')
    def test_request_publication(self, emit_mock):
        emit_mock('request_publication')
