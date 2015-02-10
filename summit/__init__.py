from flask import Flask,request,render_template,send_file,send_from_directory
from flask_admin import Admin, BaseView, expose
from flask_geoip import GeoIP
from functools import wraps, update_wrapper
from datetime import datetime
from database import db_session
import bbcode, slugify

app = Flask(__name__)
app.jinja_env.filters['bbcode'] = bbcode.render_html
app.jinja_env.filters['slugify'] = slugify.slugify

admin = Admin(app)

# sql.mit.edu's version of Flask doesn't support teardown_appcontext
@app.teardown_request
def shutdown_session(exception=None):
  db_session.remove()

# front page
from views.home import home
app.register_blueprint(home)

# static content that needs only templating (e.g. about, venue, etc.)
from views.pages import pages
app.register_blueprint(pages)

# photo gallery
from views.photos import photos
app.register_blueprint(photos,url_prefix='/photos')

# conference program from database
from views.program import program
app.register_blueprint(program,url_prefix='/program')

# sponsor page from database
from views.sponsors import sponsors
app.register_blueprint(sponsors,url_prefix='/sponsors')

# team page from database
from views.team import team
app.register_blueprint(team,url_prefix='/team')

# static media files (e.g. javascript, css, images, fonts, and static html files)
@app.route('/static/<path:filename>')
def send_foo(filename):
  return send_from_directory('/static', filename)

@app.after_request
def add_header(response):
  if(response.headers['Content-Type'].find('image/')==0):
    response.headers['Cache-Control'] = 'max-age=3600, must-revalidate'
    response.headers['Expires'] = '0'
  elif(response.headers['Content-Type'].find('application/')==0):
    response.headers['Cache-Control'] = 'max-age=3600, must-revalidate'
    response.headers['Expires'] = '0'
  else:
    response.headers['Cache-Control'] = 'max-age=300, must-revalidate'
    response.headers['Expires'] = '0'
  return response

# local development server with debug features
# (deployment is via fcgi which ignores this)
if __name__ == '__main__':
  print(app.url_map)
  app.run(debug=True)
