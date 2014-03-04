from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *

from sqlalchemy import desc

import json
import datetime, time

program = Blueprint('program', __name__,template_folder='../template')

@program.route('/', defaults={'year': ''})
@program.route('/<year>')
def show(year):
  try:

    if year=='':
      year = '2014'

    eventQuery = Event.query.filter(Event.name == year)
    if(eventQuery.count()==1):
      # the requested program exists (e.g. /program/2012)
      event = eventQuery.first()
    else:
      # invalid or non-Summit year (e.g. /program/1980 or /program/blah)
      abort(404)

    subnavbar=[]
    for e in Event.query.order_by(desc(Event.name)).all():
      subnavbar.append(('/program/'+e.name,e.name,e.name))
    subnavbar_current=year;

    program_html = ''
    program_html += '<div class="program">'
    timeslot_last = 0
    for timeslot in event.timeslot:
      if(timeslot_last==0 or timeslot.time_start.strftime("%Y%m%d")!=timeslot_last.time_start.strftime("%Y%m%d")):
        program_html += '<div class="program_row">'
        program_html += '<div class="program_date">'
        program_html += timeslot.time_start.strftime("%A, %e %B %Y")
        program_html += '</div>'
        program_html += '</div>'
      timeslot_last = timeslot
      program_html += '<div class="program_row">'
      program_html += '<div class="program_time">%s</div>' % timeslot.time_start.strftime("%H:%M")
      program_html += '<div class="program_timeslot">'
      for session in timeslot.session:
        program_html += '<div class="program_session">'
        program_html += '<div class="program_session_name">%s</div>' % session.name
#        program_html+='<div class="program_cell_session_description">%s</div>' % session.description
        program_html += '</div>'
      program_html += '</div>'
      program_html += '</div>'
    program_html += '</div>'

    program_html += '<br/><br/>'

    for timeslot in event.timeslot:
      for session in timeslot.session:
        if session.description.strip() != "":
          program_html += '<h3>%s</h3>' % session.name
          program_html += session.description
          program_html += '<br><br>'
    return render_template('page.html',title='Program',content=program_html,subnavbar=subnavbar,subnavbar_current=subnavbar_current)
  except IOError:
    abort(404)
  except TemplateNotFound:
    abort(404)
