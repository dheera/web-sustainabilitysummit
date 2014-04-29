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
  # find out which years have sponsor data in database
  eventQuery = Event.query.join(Sponsorship).group_by(Event).order_by(desc(Event.name)).having(func.count(Sponsorship.id)>0).all()

  # generate the subnavbar by year
  subnavbar=list(('/sponsors/'+e.name,e.name,e.name) for e in eventQuery)

  # decide which year is being requested based on URL or default to current year
  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  # query for that year
  event = Event.query.filter(Event.name == year).first()

  return render_template('sponsors.html',title='Sponsors',sponsorship_list=event.sponsorship,subnavbar=subnavbar,subnavbar_current=year)
