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

  # sort the timeslots in case they were entered not in order
  timeslot_list = sorted(list(event.timeslot), key=lambda x:x.time_start)

  return render_template('program.html',title='Program',timeslot_list=timeslot_list,subnavbar=subnavbar,subnavbar_current=year)

