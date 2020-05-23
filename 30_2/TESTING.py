from sort import *
import re
import unittest
import sqlite3
import cgi
import sys
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from io import StringIO, BytesIO, BufferedReader
from socketserver import BaseServer

def run_amock(app,data):

    class MockServer(WSGIServer):
        ''' Фіктивний Non-socket HTTP сервер'''
        def __init__(self, server_address, RequestHandlerClass):
            BaseServer.__init__(self, server_address, RequestHandlerClass)
            self.server_bind()
        def server_bind(self):
            host, port = self.server_address
            self.server_name = host
            self.server_port = port
            self.setup_environ()

    class MockHandler(WSGIRequestHandler):
        ''' Фіктивний Non-socket HTTP обробник'''

        def setup(self):
            self.connection = self.request
            self.rfile, self.wfile = self.connection

        def finish(self):
            pass

    server = make_server('', 8000, app, MockServer, MockHandler)

    inp = BufferedReader(BytesIO(data))
    out = BytesIO()
    olderr = sys.stderr
    err = sys.stderr = StringIO()
    try:
        server.finish_request((inp, out), ('127.0.0.1', 8000))
    finally:
        sys.stderr = olderr
    return out.getvalue(), err.getvalue()


def get_status(response):
    return re.search(r'(?P<STATUS>\d{3} .+?)\n', response).group('STATUS').rstrip()





class TestCorrectResponse(unittest.TestCase):

    def test_1_correct_path_status(self):
        request = b'GET / HTTP/1.0\n'
        out, err = run_amock(application, request)
        response = str(out, encoding='utf-8')
        status = get_status(response)
        self.assertEqual(status, '200 OK')

    def test_2_incorrect_path_status(self):
        request = b'GET /incorrect/path HTTP/1.0\n'
        out, err = run_amock(application, request)
        response = str(out, encoding='utf-8')
        status = get_status(response)
        self.assertEqual(status, '404 NOT FOUND')
    def test_3_correct_path_main(self):
        request = b'GET / HTTP/1.0\n'
        out, err = run_amock(application, data=request)
        response = str(out, encoding='utf-8')
        probablepage=response[155:len(response)]
        with open("templates/findbook.html", encoding='utf-8') as f:
            page = f.read()
        self.assertEqual(probablepage[0:200],page[0:200])
    def test_4_correct_path_other(self):
        request = b'GET /add HTTP/1.0\n'
        out, err = run_amock(application, request)
        response = str(out, encoding='utf-8')
        status = get_status(response)
        self.assertEqual(status, '200 OK')
    def test5_not_enough_info(self):
        falseinput = bytes('author={}'.format("vfd"),encoding='utf-8')
        request = (b'POST /add HTTP/1.0\n'b'Content-Type: application/x-www-form-urlencoded\n\n' +falseinput)
        out, err = run_amock(application, request)
        response = str(out, encoding='utf-8')
        print(response)
        self.assertEqual(True,"Not enough info" in response)
unittest.main(verbosity=2)