from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new

REDIRECT_URL = 'http://localhost:8080/'
PORT = 8080


class BoxLoginError(RuntimeError):

    def __init__(self, error_message):
        super(BoxLoginError, self).__init__()
        self.error_message = error_message
        pass

    def __str__(self):
        return self.error_message


def get_access_token_from_url(url):
    """
    Parse the access token from Box's response
    Args:
        uri: the box api oauth URI containing valid state
             and code arguments
    Returns:
        csrf_token
        a string containing the access key
    """
    token = str(urlopen(url).read(), 'utf-8')
    return token.split('=')[1].split('&')[0]


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
        if 'code' in self.path:
            self.auth_code = self.path.split('=')[1]
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                                   + '</h1></html>', 'utf-8'))
            self.server.access_token = self.auth_code
        elif 'error_message' in self.path:
            self.server.access_error = self.error_message

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
