from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib

from src.socket_client import SocketClient
from configs import services


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('web/index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('web/message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('web/error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))

        sock_client = SocketClient(services.UDP_IP, services.UDP_PORT)
        sock_client.send_to(data)
        sock_client.close()

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


def run(ip, port, server_class=HTTPServer, handler_class=HttpHandler):

    server_address = (ip, port)
    http = server_class(server_address, handler_class)
    try:
        print('Start Web Server')
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
