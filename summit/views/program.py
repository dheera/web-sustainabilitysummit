from flask import Response, Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached
from summit.slugify import slugify

import bbcode

from sqlalchemy import desc, func
from sqlalchemy.orm import subqueryload

import json
import datetime, time, os
from subprocess import call

program = Blueprint('program', __name__,template_folder='../template')

@program.route('/badges.csv', defaults={'year': ''})
@program.route('/<year>/badges.csv')
def get_csv(year):
  eventQuery = Event.query.join(Team).group_by(Event).order_by(desc(Event.name)).having(func.count(Team.id)>0).all()
  subnavbar=list(('/team/'+e.name,e.name,e.name) for e in eventQuery)
  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  event = Event.query.filter(Event.name == year).first()
  content = ''
  content += 'lastname,firstname,title,org,type,typebg'
  content += "\n"
  for timeslot in event.timeslot:
    for session in timeslot.session:
      for person in session.person:
        content += '%s,%s,"%s","%s",SPEAKER,#00A000' % (person.lastname.strip(), person.firstname.strip(), person.title.strip(), person.org.strip())
        content += "\n"
  return Response(content,mimetype='text/csv')

@program.route('/', defaults={'year': ''})
@program.route('/<year>')
def show(year):
  
  # find out which years have program data in database
  eventQuery = Event.query.join(Timeslot).group_by(Event).order_by(desc(Event.name)).having(func.count(Timeslot.id)>0).all()

  # generate the subnavbar by year
  subnavbar=list(('/program/'+e.name,e.name,e.name) for e in eventQuery)

  # decide which year is being requested based on URL or default to current year
  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  # query for that year
  event = Event.query.filter(Event.name == year).first()

  # filter out empty timeslots
  timeslot_list = list(filter(lambda x:len(x.session)>0, list(event.timeslot)))

  # sort the timeslots in case they were entered not in order
  timeslot_list = sorted(list(timeslot_list), key=lambda x:x.time_start)

  return render_template('program.html',title='Program',timeslot_list=timeslot_list,subnavbar=subnavbar,subnavbar_current=year)

