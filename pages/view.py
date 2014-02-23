from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import json

pages = Blueprint('pages', __name__,template_folder='../template')

@pages.route('/<pages>')
def show(pages):
  try:
    json_data=open('pages/content/%s.json' % pages).read()
    print 'Loaded'
    data = json.loads(json_data)
    print 'JSON decoded'
    return render_template('page.html',title=data['title'],content=data['content'])
  except IOError:
    abort(404)
  except TemplateNotFound:
    abort(404)
