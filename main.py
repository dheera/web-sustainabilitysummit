from flask import Flask,request,render_template

from home.view import home
from pages.view import pages
from photos.view import photos
from program.view import program

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(pages)
app.register_blueprint(photos,url_prefix='/photos')
app.register_blueprint(program,url_prefix='/program')

@app.route('/static/<path:filename>')
def send_foo(filename):
  return send_from_directory('/static', filename)

if __name__ == '__main__':
  print app.url_map
  app.run(debug=True)
