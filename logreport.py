'''
    TO DO
    1. Add SQL connection
'''
#import 
from http.server import HTTPServer, BaseHTTPRequestHandler
from logDb import get_posts
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
        html = HTML_WRAP % str(posts)
        for t in posts:
            # for i in t:
            self.wfile.write((str(t[0]) + ' ' + str(t[1]) + '\n').encode())
        # self.wfile.write(str(posts).encode())
        return html
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()


    #Second Query
    # select distinct a.name, a.id, b.author, b.title from authors a inner join articles b on a.id = b.author right join toptitle c on b.slug = c.title;