# one-time script to import the old JSON data into new model

from database import db_session
from models import *
import json
import re

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

program_json=open('/mit/summit/data/sessions.json').read();
program=json.loads(program_json);

speakers_json=open('/mit/summit/data/speakers.json').read();
speakers=json.loads(speakers_json);

session_id_conv={}

for event_name in sorted(program):
  print "... adding Event event_name=%s" % event_name
  db_session.add(Event(name=event_name))
  db_session.commit()
  last_event = Event.query.filter(Event.name == event_name).first()
  for timeslot in program[event_name]:
    print "... adding Timeslot time_start=%s" % timeslot['time']
    db_session.add(Timeslot(event_id=last_event.id,time_start=timeslot['time']))
    db_session.commit()
    last_timeslot = Timeslot.query.filter(Timeslot.time_start == timeslot['time']).first()
    if('subsessions' in timeslot):
      for session in timeslot['subsessions']:
        print "... adding Session %s" % session['title']
        if 'description' in session:
          description = session['description']
        else:
          description=''
        db_session.add(Session(timeslot_id=last_timeslot.id,name=session['title'],description=description))
        db_session.commit()
        last_session = Session.query.filter(Session.name == session['title'] and Session.timeslot_id == last_timeslot.id).first()
        session_id_conv[event_name+'/'+session['id']] = last_session
        print(event_name+'/'+session['id']+'   '+session['title'])
    else:
      print "... adding Session %s" % timeslot['title']
      if 'description' in timeslot:
        description = timeslot['description']
      else:
        description=''
      db_session.add(Session(timeslot_id=last_timeslot.id,name=timeslot['title'],description=description))
      db_session.commit()
      last_session = Session.query.filter(Session.name == timeslot['title'] and Session.timeslot_id == last_timeslot.id).first()
      session_id_conv[event_name+'/'+timeslot['id']] = last_session
      print(event_name+'/'+timeslot['id']+'   '+timeslot['title'])

for event_name in sorted(speakers):
  for speaker in speakers[event_name]:
    print "adding Person %s" % speaker['name']
    firstname, lastname = speaker['name'].rsplit(' ',1)
    try:
      title, org = speaker['title'].split(',',1)
    except:
      try:
        title, org = speaker['title'].split(' at ',1)
      except:
        title, org = speaker['title'].split(' of ',1)
    title=title.strip();
    org=org.strip();
    if 'description' in speaker:
      description = speaker['description']
    else:
      description=''
    p = Person(lastname=lastname,firstname=firstname,title=title,org=org,description=description)
#    try:
    session_id_conv[event_name+'/'+speaker['session']].person.append(p);
#    except:
#      print('error adding person to session')
    db_session.add(p);
    db_session.commit()
#    last_person = Person.query.filter(Person.lastname==lastname and Person.firstname==firstname).first()

#    FOO associate person with sessions

