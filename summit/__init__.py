from flask import Flask,request,render_template
from database import db_session
#from flask.ext.mobility import Mobility

app = Flask(__name__)
#Mobility(app)

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

# team page from database
from views.team import team
app.register_blueprint(team,url_prefix='/team')

# static media files (e.g. javascript, css, images, fonts, and static html files)
@app.route('/static/<path:filename>')
def send_foo(filename):
  return send_from_directory('/static', filename)

# local development server with debug features
# (deployment is via fcgi which ignores this)
if __name__ == '__main__':
  print(app.url_map)
  app.run(debug=True)
