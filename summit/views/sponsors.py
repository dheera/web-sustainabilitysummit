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
      sponsors_html += sponsor.name+'<br>'

  return render_template('page.html',title='Sponsors',content=sponsors_html,subnavbar=subnavbar,subnavbar_current=year)
