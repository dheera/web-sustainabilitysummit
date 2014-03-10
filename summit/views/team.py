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
def show(year):

  eventQuery = Event.query.join(Team).group_by(Event).order_by(desc(Event.name)).having(func.count(Team.id)>0).all()

  subnavbar=list(('/team/'+e.name,e.name,e.name) for e in eventQuery)

  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  event = Event.query.filter(Event.name == year).first()

  content=''

  for team in event.team:
    content += '<h2>%s</h2>' % team.name

    for person in team.person:
      content += '<div class="team_person">'
      content += '<div class="team_person_picture"><img src="'+person.get_picture_url(size='120x120')+'"></div>'
      content += '<div class="program_person_cell">'
      content += '<div class="program_person_name">%s %s</div>' % (person.firstname, person.lastname)
      if(not team.name):
        content += '<div class="program_person_titleorg">%s</div>' % person.title
      if(person.description):
        content += '<div class="team_person_description">%s</div>' % person.description
      content += '</div>'
      content += '</div>'

      content += '<div class="team_mobile_person clickable" onclick="$(this).next(\'.team_mobile_person_description_wrapper\').slideToggle()">'
      content += '<div class="team_mobile_person_picture"><img src="'+person.get_picture_url(size='120x120')+'"></div>'
      content += '<div class="team_mobile_person_cell">'
      content += '<div class="program_person_name">%s %s</div>' % (person.firstname, person.lastname)
      if(not team.name):
        content += '<div class="program_person_titleorg">%s</div>' % person.title
      content += '</div>'
      content += '</div>'
      if(person.description):
        content += '<div class="team_mobile_person_description_wrapper">'
        content += '<div class="team_mobile_person_description">%s</div>' % person.description
        content += '</div>'
      content += '<br><br>'

  return render_template('page.html',title='Team',content=content,subnavbar=subnavbar,subnavbar_current=year)
