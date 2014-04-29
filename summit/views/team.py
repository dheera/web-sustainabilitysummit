from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached

from sqlalchemy import desc, func
from sqlalchemy.orm import subqueryload
from subprocess import call

import json

team = Blueprint('team', __name__,template_folder='../template')

@team.route('/', defaults={'year': ''})
@team.route('/<year>')
@cached()
def show(year):
  # find out which years have team data in database
  eventQuery = Event.query.join(Team).group_by(Event).order_by(desc(Event.name)).having(func.count(Team.id)>0).all()

  # generate the subnavbar by year
  subnavbar=list(('/team/'+e.name,e.name,e.name) for e in eventQuery)

  # decide which year is being requested based on URL or default to current year
  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  # query for that year
  event = Event.query.filter(Event.name == year).first()

  return render_template('team.html',title='Team',team_list=event.team,subnavbar=subnavbar,subnavbar_current=year)
