from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached

from sqlalchemy import desc, func
from sqlalchemy.orm import subqueryload
from subprocess import call

import json

sponsors = Blueprint('sponsors', __name__,template_folder='../template')

@sponsors.route('/', defaults={'year': ''})
@sponsors.route('/<year>')
@cached()
def show(year):

  eventQuery = Event.query.join(Sponsorship).group_by(Event).order_by(desc(Event.name)).having(func.count(Sponsorship.id)>0).all()

  subnavbar=list(('/sponsors/'+e.name,e.name,e.name) for e in eventQuery)

  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  event = Event.query.filter(Event.name == year).first()

  sponsors_html=''

  for sponsorship in event.sponsorship:
    sponsors_html += '<h2>%s</h2>' % sponsorship.name

    for sponsor in sponsorship.sponsor:
      vector_url = sponsor.get_logo_vector_url()
      raster_url = sponsor.get_logo_raster_url()

      if(False and vector_url): # until we find a workaround for Chrome <object> bug which has been around for years
        sponsors_html += '<div class="sponsor" style="cursor:pointer;cursor:hand;" onclick="window.location.href=\'%s\';">' % sponsor.url
        sponsors_html += '<div class="ui_cover" style="width:210px;height:110px;"></div>'
        sponsors_html += '<object alt="%s" data="%s" type="image/svg+xml" width="210" height="110"><param name="src" value="%s">' % (sponsor.name, vector_url, vector_url);
        sponsors_html += '<img alt="%s" width="210" height="110" src="%s">' % (sponsor.name, raster_url);
        sponsors_html += '</object>'
        sponsors_html += '</div> '
      elif(raster_url):
        sponsors_html += '<div class="sponsor clickable" onclick="window.location.href=\'%s\';">' % sponsor.url
        sponsors_html += '<div class="ui_cover" style="width:210px;height:110px;"></div>'
        sponsors_html += '<img alt="%s" style="width:210px;height:110px;" src="%s">' % (sponsor.name, raster_url);
        sponsors_html += '</div> '
      else:
        sponsors_html += '<div class="sponsor clickable" onclick="window.location.href=\'%s\';">' % sponsor.url
        sponsors_html += '<div>'
        sponsors_html += sponsor.name
        sponsors_html += '</div>'
        sponsors_html += '</div> '

  return render_template('page.html',title='Sponsors',content=sponsors_html,subnavbar=subnavbar,subnavbar_current=year)
