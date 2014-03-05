from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached
from summit.slugify import slugify

from subprocess import call

import os, glob;

import json

PHOTOS_DIR = 'summit/static/photos'

photos = Blueprint('photos', __name__,template_folder='../template')

@photos.route('/', defaults={'year': ''})
@photos.route('/<year>')
def show(year):
  dirs = [ name for name in os.listdir(PHOTOS_DIR) if os.path.isdir(os.path.join(PHOTOS_DIR, name)) ]
  subnavbar = [ ('/photos/'+name, name, name) for name in sorted(dirs,reverse=True) ]

  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in dirs:
      abort(404)

  photos_html = ''

  for image_file in glob.glob("%s/%s/*.jpg" % (PHOTOS_DIR,year)):
    image_url = image_file.replace('summit','')

    thumb_size = '154x154'
    thumb_file = 'summit/static/cache/'+slugify(image_url)+'-'+thumb_size+'.jpg'
    thumb_url = thumb_file.replace('summit','')

    if not os.path.exists(thumb_file):
      call(["convert", "-strip", image_file, "-thumbnail", thumb_size+"^", "-gravity", "center", "-quality", "83", "-extent", thumb_size, thumb_file])

    photos_html += "<div class=\"photos_thumbnail clickable\">"
    photos_html += "<a title=\"\" class=\"swipebox\" href=\"%s\"><img src=\"%s\"></a>" % (image_url, thumb_url)
    photos_html += "</div> " # trailing space after </div> is important! we are using inline-block

  return render_template('page.html',title='Photos',content=photos_html,subnavbar=subnavbar,subnavbar_current=year)
