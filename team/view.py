from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import json

team = Blueprint('team', __name__,template_folder='../template')

@team.route('/', defaults={'page': 'index'})
@team.route('/<page>')
def show(page):
  return 'foo '+self.url_prefix
  try:
    json_data=open('team/content/%s.json' % page).read()
    data = json.loads(json_data)
    return render_template('team.html',title=data['title'],content=data['content'])
  except IOError:
    abort(404)
  except TemplateNotFound:
    abort(404)
