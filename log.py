from flask import Flask, request, redirect, url_for
from logDb import get_posts
#from forumdb_initial import get_posts, add_post

app = Flask(__name__)

#HTML template for Forum page

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
    <head>
       <title> News Log Report</title>
       <style>
        


       </style> 
    </head>
    <body>
        <h1>News Logs</h1>
        <form method = post>
        </form>
%s

    </body>
</html>
'''

@app.route('/', methods=['GET'])
def main():
    '''Main Page of News Log'''
    print("Revanth")
    post = get_posts
    print(post)
    html = HTML_WRAP % post
    return html

@app.route('/', methods=['POST'])
def post():
    
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
