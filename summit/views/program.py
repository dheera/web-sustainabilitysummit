from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from summit.database import db_session
from summit.models import *
from summit.cache import cached
from summit.slugify import slugify

from sqlalchemy import desc, func
from sqlalchemy.orm import subqueryload

import json
import datetime, time, os
from subprocess import call

program = Blueprint('program', __name__,template_folder='../template')

@program.route('/', defaults={'year': ''})
@program.route('/<year>')
@cached()
def show(year):

  eventQuery = Event.query.join(Timeslot).group_by(Event).order_by(desc(Event.name)).having(func.count(Timeslot.id)>0).all()

  subnavbar=list(('/program/'+e.name,e.name,e.name) for e in eventQuery)

  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  event = Event.query.filter(Event.name == year).first()

  program_html = ''

  program_html += '<div class="program_mobile">'
  timeslot_last = 0
  for timeslot in event.timeslot:
    if(timeslot_last==0 or timeslot.time_start.strftime("%Y%m%d")!=timeslot_last.time_start.strftime("%Y%m%d")):
      program_html += '<div class="program_row">'
      program_html += '<div class="program_date">'
      program_html += timeslot.time_start.strftime("<b>%A</b> %e %B %Y")
      program_html += '</div>'
      program_html += '</div>'
    timeslot_last = timeslot

    for session in timeslot.session:
      if session.description!='':
        program_html += '<div class="clickable program_mobile_row_clickable" onclick="$(this).next(\'.program_mobile_session_description\').slideToggle()">'
      else:
        program_html += '<div class="program_mobile_row">'
      program_html += '<div class="program_mobile_icon"></div>'
      program_html += '<div class="program_mobile_time">%s</div>' % timeslot.time_start.strftime("%H:%M")
      program_html += '<div class="program_mobile_session">%s</div>' % session.name
      program_html += '</div>'
      if session.description!='':
        program_html += '<div class="program_mobile_session_description">'
        program_html += session.description
        for person in session.person:
          program_html += '<div class="clickable program_mobile_session_person" onclick="$(this).next(\'.program_mobile_session_person_description\').slideToggle()">'
          program_html += '<img src="%s" style="width:60px;height:60px;float:left;margin-right:15px;margin-top:5px;">' % person.get_picture_url(size='60x60')
          program_html += '<b>%s %s</b><br>%s, %s' % (person.firstname, person.lastname, person.title, person.org)
          program_html += '</div>'
          program_html += '<div class="program_mobile_session_person_description">'
          program_html += person.description
          program_html += '</div>'
        program_html += '</div>'

  program_html += '</div>'

  program_html += '<div class="program">'
  timeslot_last = 0
  for timeslot in event.timeslot:
    if(timeslot_last==0 or timeslot.time_start.strftime("%Y%m%d")!=timeslot_last.time_start.strftime("%Y%m%d")):
      program_html += '<div class="program_row">'
      program_html += '<div class="program_date">'
      program_html += timeslot.time_start.strftime("<b>%A</b> %e %B %Y")
      program_html += '</div>'
      program_html += '</div>'
    timeslot_last = timeslot
    program_html += '<div class="program_row">'
    program_html += '<div class="program_time">%s</div>' % timeslot.time_start.strftime("%H:%M")
    program_html += '<div class="program_timeslot">'
    for session in timeslot.session:
      if session.description.strip() != "" or len(session.person)>0:
        program_html += '<div class="clickable program_session" onclick="window.location.href=\'#%s\'">' % slugify(session.name)
        program_html += '<span style="font-size:12px;"><a href="#%s">READ MORE &raquo;</a></span>' % slugify(session.name)
      else:
        program_html += '<div class="program_session">'
      program_html += '<div class="program_session_name">%s</div>' % session.name
      program_html += '</div>'

    program_html += '</div>'
    program_html += '</div>'

  program_html += '<br><br>'
  program_html += '<h2>Session descriptions</h2><br>'

  for timeslot in event.timeslot:
    for session in timeslot.session:
      if session.description.strip() != "" or len(session.person)>0:
        program_html += '<a name="%s"></a>' % slugify(session.name)
        program_html += '<div class="clickable program_backtotop" onclick="window.location.href=\'#\'"></div>' 
        program_html += '<h3>%s</h3>' % session.name
        program_html += session.description
        for person in session.person:
          program_html += '<div class="program_person">'
          program_html += '<div class="program_person_cell"><img src="'+person.get_picture_url(size='120x120')+'"></div>'
          program_html += '<div class="program_person_cell">'
          program_html += '<div class="program_person_name">%s %s</div>' % (person.firstname, person.lastname)
          program_html += '<div class="program_person_titleorg">%s, %s</div>' % (person.title.upper(), person.org)
          if(person.description):
            program_html += '<div class="program_readdescription clickable" onclick="$(this).next(\'.program_person_description\').slideToggle()"></div>'
          program_html += '<div class="program_person_description">%s</div>' % person.description
          program_html += '</div>'
          program_html += '</div>'
        program_html += '<br><br>'

  program_html += '</div>'

  return render_template('page.html',title='Program',content=program_html,subnavbar=subnavbar,subnavbar_current=year)
