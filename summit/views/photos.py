from flask import Blueprint, render_template, abort, Response, send_file, send_from_directory
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached
from summit.slugify import slugify

from subprocess import call

import os, glob;

import json

PHOTOS_DIR = 'summit/static/photos'
CACHE_DIR = 'summit/static/cache'

photos = Blueprint('photos', __name__,template_folder='../template')

@photos.route('/<album>/<photo>/<size>/')
def get_photo_resized(album,photo,size):
  allowed_sizes = ['154x154','300x200','600x400']

  if '..' in album or album.startswith('/'):
    abort(404)
  if '..' in photo or photo.startswith('/'):
    abort(404)
  if size not in allowed_sizes:
    abort(404)

  image_file = PHOTOS_DIR + '/' + album + '/' + photo
  thumb_file = CACHE_DIR + '/photos-'+slugify(album+'-'+photo)+'-'+size+'.jpg'
  thumb_url = 'static/cache/photos-'+slugify(album+'-'+photo)+'-'+size+'.jpg'

  if not os.path.exists(thumb_file):
    call(["convert", "-strip", image_file, "-thumbnail", size+"^", "-gravity", "center", "-quality", "83", "-extent", size, thumb_file])

  return send_file('../'+thumb_file)


@photos.route('/<path:album>/<path:photo>')
def get_photo(album,photo):
  if '..' in album or album.startswith('/'):
    abort(404)
  if '..' in photo or photo.startswith('/'):
    abort(404)

  image_file = PHOTOS_DIR + '/' + album + '/' + photo
  return send_file('../' + image_file)

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
    image_url = '/photos' + image_file.replace(PHOTOS_DIR,'')
    thumb_url = image_url + '/154x154'
    #thumb_size = '154x154'
    #thumb_file = 'summit/static/cache/'+slugify(image_url)+'-'+thumb_size+'.jpg'
    #thumb_url = thumb_file.replace('summit','')

    #if not os.path.exists(thumb_file):
    #  call(["convert", "-strip", image_file, "-thumbnail", thumb_size+"^", "-gravity", "center", "-quality", "83", "-extent", thumb_size, thumb_file])

    photos_html += "<div class=\"photos_thumbnail clickable\">"
    photos_html += "<a title=\"\" class=\"swipebox\" href=\"%s\"><img src=\"%s\"></a>" % (image_url, thumb_url)
    photos_html += "</div> " # trailing space after </div> is important! we are using inline-block

  return render_template('page.html',title='Photos',content=photos_html,subnavbar=subnavbar,subnavbar_current=year)
