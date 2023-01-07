from unittest import TestCase
from urllib.parse import parse_qs
from json import loads, dumps

from src.cgiw.decorators import body_parser

class TestDecorators(TestCase):
    def test_body_parser_qs(self):

        @body_parser(parse_qs)
        def post_handler(query, headers, body):
            assert isinstance(body, dict)
            return ('', {}, '')
        
        post_handler({}, {}, 'hello=world')

    def test_body_parser_json(self):
        @body_parser(loads)
        def post_handler(query, headers, body):
            assert isinstance(body, dict)
            return ('', {}, '')
        
        post_handler({}, {}, dumps({'hello': 'world'}))
