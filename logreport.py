'''
    TO DO
    1. Add SQL connection
'''
#import 
from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        self.wfile.write("Hello, My First Project! \n Hope you will be successful".encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()