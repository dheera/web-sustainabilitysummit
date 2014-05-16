from flask import Flask,request,render_template,send_file,send_from_directory
from jinja2 import Markup
from flask_admin import Admin, BaseView, expose
from flask_geoip import GeoIP
from functools import wraps, update_wrapper
from datetime import datetime
from database import db_session

from summit.slugify import slugify
import bbcode

app = Flask(__name__)

# get rid of extraneous white space in HTML
app.jinja_options['extensions'].append('jinja2htmlcompress.HTMLCompress')

# additional jinja2 filters we will use in templates

def render_bbcode(code):
  return Markup(bbcode.render_html(code))

app.jinja_env.filters['bbcode'] = render_bbcode
app.jinja_env.filters['slugify'] = slugify

# admin interface (under construction)
admin = Admin(app)

# sql.mit.edu's version of Flask doesn't support teardown_appcontext
@app.teardown_request
def shutdown_session(exception=None):
  db_session.remove()

# front page
from views.home import home
app.register_blueprint(home)

# static pages that need only templating (e.g. about, venue, etc.)
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

# adjust client side caching
@app.after_request
def add_header(response):
  if(response.headers['Content-Type'].find('image/')==0):
    # tell client to cache images for 2 hours
    response.headers['Cache-Control'] = 'max-age=7200, must-revalidate'
    response.headers['Expires'] = '0'
  elif(response.headers['Content-Type'].find('application/')==0):
    # tell client to cache downloads for 2 hours
    response.headers['Cache-Control'] = 'max-age=7200, must-revalidate'
    response.headers['Expires'] = '0'
  else:
    # tell client to cache everything else (especially text/html) for 5 minutes only
    # in case urgent updates to content need to be made
    response.headers['Cache-Control'] = 'max-age=300, must-revalidate'
    response.headers['Expires'] = '0'
  return response

# local development server with debug features
# (deployment is via fcgi which ignores this)
if __name__ == '__main__':
  print(app.url_map)
  app.run(debug=True)
