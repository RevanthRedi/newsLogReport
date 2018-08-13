'''
    TO DO
    1. Add SQL connection
'''
#import 
from http.server import HTTPServer, BaseHTTPRequestHandler
from logDb import get_posts, get_posts1, get_posts2
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB Forum</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>DB Forum</h1>
    <form method=post>
      <div><textarea id="content" name="content"></textarea></div>
      <div><button id="go" type="submit">Post message</button></div>
    </form>
    <!-- post content will go here -->
%s
    
%s

%s
  </body>
</html>
'''

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        # get_posts()
        posts = get_posts()
        posts1 = get_posts1()
        posts2 = get_posts2()
        html = HTML_WRAP % (str(posts), str(posts1), str(posts2))
        self.wfile.write("1. Top three artilces\n\n".encode())
        self.wfile.write("-----------------------------------\n".encode())
        for t in posts:
            # for i in t:
          
          self.wfile.write((str(t[0]) + '\t | \t ' + str(t[1]) + '\n\n').encode())
        # self.wfile.write(str(posts).encode())
        self.wfile.write("------------------------------------------\n".encode())
        self.wfile.write("2. Authors of top 3 articles\n\n".encode())
        for l in posts1:
          self.wfile.write((str(l[0]) + ' \t | \t ' + str(l[1]) + '\n').encode())
        self.wfile.write("------------------------------------------\n".encode())
        self.wfile.write("3. On which days did more than 1% of requests lead to errors? \n\n".encode())
        for m in posts2:

          self.wfile.write((str(m[0]) + '\t | \t' + str(m[1]) + '\n').encode())
        return html


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()
