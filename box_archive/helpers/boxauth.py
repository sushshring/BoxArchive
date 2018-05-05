from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
import urllib.parse as parse
from webbrowser import open_new

import logging

logger = logging.getLogger('box_archive')

REDIRECT_URL = 'http://localhost:8080/'
PORT = 8080


class BoxLoginError(RuntimeError):

    def __init__(self, error_message):
        super(BoxLoginError, self).__init__()
        self.error_message = error_message
        pass

    def __str__(self):
        return self.error_message


def get_access_token_from_url(path):
    """
    Parse the access token from Box's response
    Args:
        path: the box api oauth URI path containing valid state
             and code arguments
    Returns:
        dict containing parsed url parameters
    """
    return parse.parse_qs(path)


class HTTPServerHandler(BaseHTTPRequestHandler):
    """
    HTTP Server callbacks to handle Box OAuth redirects
    """

    def __init__(self, request, address, server, access_uri):
        self.access_uri = access_uri
        BaseHTTPRequestHandler.__init__(self, request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        result = get_access_token_from_url(self.path)
        if 'code' in result:
            self.auth_code = result['code'][0]
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                                   + '</h1></html>', 'utf-8'))
            self.server.access_token = self.auth_code
        elif 'error_description' in result:
            logger.debug(result['error_description'][0])
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                                   + '</h1></html>', 'utf-8'))
            self.server.access_error = result['error_description'][0]

    # Disable logging from the HTTP Server
    def log_message(self, format, *args):
        return


class TokenHandler:
    """
    Functions used to handle Box oAuth
    """

    def __init__(self):
        pass

    def get_access_token(self, access_uri):
        open_new(access_uri)
        http_server = HTTPServer(
            ('localhost', PORT),
            lambda request, address, server: HTTPServerHandler(
                request, address, server, access_uri))
        http_server.handle_request()
        try:
            return http_server.access_token
        except AttributeError:
            raise BoxLoginError(error_message=http_server.access_error)
