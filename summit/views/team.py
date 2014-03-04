from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached

from sqlalchemy import desc
from sqlalchemy.orm import subqueryload
from subprocess import call

import json

team = Blueprint('team', __name__,template_folder='../template')

@team.route('/', defaults={'year': ''})
@team.route('/<year>')
def show(year):
  if year=='':
    year = '2014'

  eventQuery = Event.query.filter(Event.name == year)
  if(eventQuery.count()==1):
    event = eventQuery.first()
  else:
    abort(404)

  subnavbar=[]
  for e in Event.query.order_by(desc(Event.name)).all():
    subnavbar.append(('/team/'+e.name,e.name,e.name))
  subnavbar_current=year;

  teamQuery = Team.query.filter(Team.event_id == event.id)
  if(teamQuery.count()==0):
    abort(404)

  team_html=''

  for team in teamQuery:
    team_html += '<h2>%s</h2>' % team.name

    for person in team.person:
      team_html += '<div class="program_person">'
      team_html += '<div class="program_person_cell"><img src="'+person.get_picture_url(size='120x120')+'"></div>'
      team_html += '<div class="program_person_cell">'
      team_html += '<div class="program_person_name">%s %s</div>' % (person.firstname, person.lastname)
      if(not team.name):
        team_html += '<div class="program_person_titleorg">%s, %s</div>' % (person.title.upper(), person.org)
      if(person.description):
        team_html += '<div style="display:block;" class="program_person_description">%s</div>' % person.description
      team_html += '</div>'
      team_html += '</div>'
      team_html += '<br><br>'

  return render_template('page.html',title='Team',content=team_html,subnavbar=subnavbar,subnavbar_current=subnavbar_current)
