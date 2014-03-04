from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import json

pages = Blueprint('pages', __name__,template_folder='../template')

@pages.route('/<pages>')
@pages.route('/<pages>/')
def show(pages):
  try:
    isHeaderFinished=0
    header_json=''
    content=''
    with open('summit/media/pages/' + pages) as fp:
      for line in fp:
        if(line.strip()==''):
          isHeaderFinished=1
        if(isHeaderFinished):
          content+=line.decode('utf-8')
        else:
          header_json+=line.decode('utf-8')
    print 'Loaded'
    header = json.loads(header_json)
    print 'JSON decoded'
    return render_template('page.html',title=header['title'],content=content)
  except IOError:
    abort(404)
  except TemplateNotFound:
    abort(404)
