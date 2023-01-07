from unittest import TestCase

from src.cgiw.responses import json, redirect

class TestResponses(TestCase):
    def test_json(self):
        obj = {'hello': 'world'}
        response = json(obj)
        self.assertEqual(response, ('200 OK', {'Content-Type': 'application/json'}, '{"hello": "world"}'))

    def test_redirect(self):
        url = "https://google.com/"
        response = redirect(url)
        self.assertEqual(response, ('301 Moved Permanently', {'Content-Type': 'text/plain', 'Location': 'https://google.com/'}, 'Redirecting to https://google.com/...'))