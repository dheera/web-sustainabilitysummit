from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import json

photos = Blueprint('photos', __name__,template_folder='../template')

@photos.route('/', defaults={'page': 'index'})
@photos.route('/<page>')
def show(page):
  return 'foo '+self.url_prefix
  try:
    json_data=open('photos/content/%s.json' % page).read()
    data = json.loads(json_data)
    return render_template('photos.html',title=data['title'],content=data['content'])
  except IOError:
    abort(404)
  except TemplateNotFound:
    abort(404)
