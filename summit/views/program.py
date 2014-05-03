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
  eventQuery = Event.query.join(Timeslot).group_by(Event).order_by(desc(Event.name)).having(func.count(Timeslot.id)>0).all()
  subnavbar=list(('/program/'+e.name,e.name,e.name) for e in eventQuery)
  if year=='':
    year = subnavbar[0][1]
  else:
    if not year in tuple(e.name for e in eventQuery):
      abort(404)

  event = Event.query.filter(Event.name == year).first()
  content = ''
  content += 'lastname,firstname,title,org,time_start,session,type,typebg'
  content += "\n"
  for timeslot in event.timeslot:
    for session in timeslot.session:
      for person in session.person:
        session_name_trunc = (session.name[:35] + '...') if len(session.name) > 35 else session.name
        content += '%s,%s,"%s","%s",%s,"%s",SPEAKER,#00A000' % (person.lastname, person.firstname, person.title.replace('"','""'), person.org.replace('"','""'), timeslot.time_start.strftime("%a %H:%M"), session_name_trunc)
        content += "\n"
  return Response(content,mimetype='text/csv')

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

  content = ''
  
  content += '<div class="program_mobile">'
  timeslot_last = 0
  for timeslot in event.timeslot:
    if(timeslot_last==0 or timeslot.time_start.strftime("%Y%m%d")!=timeslot_last.time_start.strftime("%Y%m%d")):
      content += '<div class="program_row">'
      content += '<div class="program_date">'
      content += timeslot.time_start.strftime("<b>%A</b> %e %B %Y")
      content += '</div>'
      content += '</div>'
    timeslot_last = timeslot

    for session in timeslot.session:
      if (session.description and session.description.strip() != "") or len(session.person)>0:
        content += '<div class="clickable program_mobile_row program_mobile_row_clickable" onclick="$(this).next(\'.program_mobile_session_description\').slideToggle();$(this).children(\'.program_mobile_icon\').toggleClass(\'program_mobile_icon_off program_mobile_icon_on\')" data-time_start="%s" data-time_end="%s">' % ( timeslot.time_start.strftime("%s"), timeslot.time_end.strftime("%s") )
        content += '<div class="program_mobile_icon program_mobile_icon_off"></div>'
      else:
        content += '<div class="program_mobile_row" data-time_start="%s" data-time_end="%s">' % ( timeslot.time_start.strftime("%s"), timeslot.time_end.strftime("%s") )
        content += '<div class="program_mobile_icon"></div>'
      content += '<div class="program_mobile_time">%s</div>' % timeslot.time_start.strftime("%H:%M")
      content += '<div class="program_mobile_session_location">'
      if (session.location and session.location.strip() != ""):
        content += session.location
      content += '</div>'
      content += '<div class="program_mobile_session">%s</div>' % session.name
      content += '</div>'
      if (session.description and session.description.strip() != "") or len(session.person)>0:
        content += '<div class="program_mobile_session_description">'
        content += bbcode.render_html(session.description)
        for person in session.person:

          content += '<div class="clickable program_mobile_session_person" onclick="$(this).next(\'.program_mobile_session_person_description\').slideToggle();">'
          content += '<div class="program_mobile_session_person_picture"><img src="%s"></div>' % person.get_picture_url(size='60x60')
          content += '<b>%s %s</b><br>%s, %s' % (person.firstname, person.lastname, person.title, person.org)
          content += '</div>'

          content += '<div class="program_mobile_session_person_description">'
          if(person.description):
            content += bbcode.render_html(person.description)
          content += '</div>'

        content += '</div>'

  content += '</div>'

  content += '<div class="program">'
  timeslot_last = 0
  for timeslot in event.timeslot:
    if(timeslot_last==0 or timeslot.time_start.strftime("%Y%m%d")!=timeslot_last.time_start.strftime("%Y%m%d")):
      content += '<div class="program_row">'
      content += '<div class="program_date">'
      content += timeslot.time_start.strftime("<b>%A</b> %e %B %Y")
      content += '</div>'
      content += '</div>'
    timeslot_last = timeslot
    content += '<div class="program_row" data-time_start="%s" data-time_end="%s">' % ( timeslot.time_start.strftime("%s"), timeslot.time_end.strftime("%s") )
    content += '<div class="program_time">%s</div>' % timeslot.time_start.strftime("%H:%M")
    content += '<div class="program_timeslot">' # data-time_start="%s" data-time_end="%s">' % ( timeslot.time_start.strftime("%s"), timeslot.time_end.strftime("%s") )
    for session in timeslot.session:
      if (session.description and session.description.strip() != "") or len(session.person)>0:
        content += '<div class="clickable program_session" onclick="window.location.href=\'#%s\'">' % slugify(session.name)
        content += '<span style="font-size:12px;"><a href="#%s">READ MORE &raquo;</a></span>' % slugify(session.name)
      else:
        content += '<div class="program_session">'
      content += '<div class="program_session_name">%s</div>' % session.name
      if (session.location and session.location.strip() != ""):
        content += '<div class="program_session_location">ROOM: <b>%s</b></div>' % session.location
      content += '</div>'

    content += '</div>'
    content += '</div>'

  content += """
<script type="text/javascript">
$(function(){
  runProgramTimer();
});

var PROGRAM_TZOFFSET=-4;

function runProgramTimer() {
  $('.program_row').each(function(){
    var now = (new Date).getTime()/1000 + PROGRAM_TZOFFSET*3600;
    if($(this).data('time_start')<now && $(this).data('time_end')>now) {
      $(this).addClass('program_row_active');
    } else {
      $(this).removeClass('program_row_active');
    }
  });
  $('.program_mobile_row').each(function(){
    var now = (new Date).getTime()/1000 + PROGRAM_TZOFFSET*3600;
    if($(this).data('time_start')<now && $(this).data('time_end')>now) {
      $(this).addClass('program_mobile_row_active');
    } else {
      $(this).removeClass('program_mobile_row_active');
    }
  });
  window.setTimeout('runProgramTimer()',20000);
}

</script>
"""

  content += '<br><br>'
  content += '<h2>Session descriptions</h2><br>'

  for timeslot in event.timeslot:
    for session in timeslot.session:
      if(session.description and session.description.strip() != "") or len(session.person)>0:
        content += '<a name="%s"></a>' % slugify(session.name)
        content += '<div class="clickable program_backtotop" onclick="window.location.href=\'#\'"></div>' 
        content += '<h3 style="padding-left:15px;border-left:15px solid #b0c0b0;">%s</h3>' % session.name
        content += bbcode.render_html(session.description)
        for person in session.person:
          content += '<div class="program_person">'
          content += '<div class="program_person_cell"><img src="'+person.get_picture_url(size='120x120')+'"></div>'
          content += '<div class="program_person_cell">'
          content += '<div class="program_person_name">%s %s</div>' % (person.firstname, person.lastname)
          content += '<div class="program_person_titleorg">%s, %s</div>' % (person.title.upper(), person.org)
          if(person.description):
            content += '<div class="program_readdescription clickable" onclick="$(this).next(\'.program_person_description\').slideToggle()"></div>'
            content += '<div class="program_person_description">%s</div>' % bbcode.render_html(person.description)
          content += '</div>'
          content += '</div>'
        content += '<br><br>'

  content += '</div>'

  return render_template('page.html',title='Program',content=content,subnavbar=subnavbar,subnavbar_current=year)

