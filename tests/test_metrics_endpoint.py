import unittest
from tornado.testing import AsyncHTTPTestCase
import tornado.web

from seesaw.web import MetricsHandler, ACTIVE_ITEMS

class MetricsEndpointTest(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application([
            (r"/metrics", MetricsHandler),
        ], auth_enabled=False, check_auth=lambda r,u,p: True, skip_auth=[], auth_realm="")

    def test_metrics_endpoint(self):
        ACTIVE_ITEMS.labels(project="test").set(1)
        response = self.fetch('/metrics')
        self.assertEqual(response.code, 200)
        body = response.body.decode('utf-8')
        self.assertIn('seesaw_active_items', body)

if __name__ == '__main__':
    unittest.main()
