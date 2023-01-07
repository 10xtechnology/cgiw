from unittest import TestCase, mock
from src.handler import Handler
from os import environ
from sys import stdin
from json import dumps
from io import StringIO
from typing import Tuple, List, Union, Dict

from src import handler


class MyHandler(Handler):
    def get(self, query: Dict[str, Union[str, List[str]]], headers: Dict[str, str]) -> Tuple[str, Dict[str, str], str]:
        return ('200 OK', {'Content-Type': 'application/json'}, dumps(query))
    
    def post(self, query: Dict[str, Union[str, List[str]]], headers: Dict[str, str], body: str) -> Tuple[str, Dict[str, str], str]:
        return ('200 OK', {'Content-Type': 'application/json'}, body)

QUERY_STRING = 'hello=world&test=123'
BODY = dumps({'foo': 'bar'})
GET_ENV = {
    'REQUEST_METHOD': 'GET',
    'QUERY_STRING': QUERY_STRING
}

POST_ENV_JSON = {
    'REQUEST_METHOD': 'POST',
    'QUERY_STRING': QUERY_STRING,
    'CONTENT_LENGTH': str(len(BODY)),
    'CONTENT_TYPE': 'application/json'
}

class TestHandler(TestCase):
    handler = MyHandler(verbose=False)

    @mock.patch.dict(environ, GET_ENV)
    def test_run_get(self):
        response = self.handler.run()
        self.assertEqual(response, f"Status: 200 OK\nContent-Type: application/json\n\n{dumps({'hello': 'world', 'test': '123'})}")

    @mock.patch.dict(environ, POST_ENV_JSON)
    def test_run_post_json(self):
        handler.stdin = StringIO(BODY)
        response = self.handler.run()
        self.assertEqual(response, f"Status: 200 OK\nContent-Type: application/json\n\n{BODY}")

    @mock.patch.dict(environ, GET_ENV)
    def test_parse_query(self):
        result = self.handler.parse_query()
        self.assertEqual(result, {
            'hello': 'world',
            'test': '123'
        })

    @mock.patch.dict(environ, POST_ENV_JSON)
    def test_parse_headers(self):
        result = self.handler.parse_headers()
        self.assertEqual(result, {
            'Content-Length': 14,
            'Content-Type': 'application/json'
        })

    def test_parse_body(self):
        handler.stdin = StringIO(BODY)
        result = self.handler.parse_body({'Content-Length': 14})
        self.assertEqual(result, BODY)

    def test_handle(self):
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': 14
        }
        result = self.handler.handle('POST', headers, {}, BODY)
        self.assertEqual(result, ('200 OK', {'Content-Type': 'application/json'}, BODY))

    def test_compose_response(self):
        result = self.handler.compose_response('200 OK', {'Content-Type': 'text/plain'}, 'hello')
        self.assertEqual(result, "Status: 200 OK\nContent-Type: text/plain\n\nhello")