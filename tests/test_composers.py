from unittest import TestCase
from random import randint

from src.cgiw.composers import compose_response


class TestComposers(TestCase):
    def test_compose_response(self):
        status = '200 OK'
        body = str(randint(1111, 999999))
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': len(body)
        }
        result = compose_response(status, headers, body)

        self.assertEqual(result, f"Status: 200 OK\nContent-Type: text/plain\nContent-Length: {len(body)}\n\n{body}")
