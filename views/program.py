from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import json

program = Blueprint('program', __name__,template_folder='../template')

@program.route('/', defaults={'page': 'index'})
@program.route('/<page>')
def show(page):
  return 'foo '+self.url_prefix
  try:
    json_data=open('program/content/%s.json' % page).read()
    data = json.loads(json_data)
    return render_template('program.html',title=data['title'],content=data['content'])
  except IOError:
    abort(404)
  except TemplateNotFound:
    abort(404)
