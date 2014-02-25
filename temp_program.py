from database import db_session
from models import *
import json

program_json=open('/mit/summit/data/sessions.json').read();
program=json.loads(program_json);

speakers_json=open('/mit/summit/data/speakers.json').read();
speakers=json.loads(speakers_json);

for event_name in sorted(program):
  print "adding Event event_name=%s" % event_name
  db_session.add(Event(name=event_name))
  for timeslot in program[event_name]:
    print "adding Timeslot time_start=%s" % timeslot['time']
    FOO db_session.add(Timeslot(event_id=0,time_start=timeslot['time']))
    if('subsessions' in timeslot):
      for session in timeslot['subsessions']:
        print "adding Session %s" % session['title']
        FOO db_session.add(Timeslot(event_id=0,time_start=timeslot['time']))
        FOO session_id_conv=[session['id']]=NEWID
    else:
      print "adding Session %s" % timeslot['title']
      FOO db_session.add(Timeslot(event_id=0,time_start=timeslot['time']))
      FOO session_id_conv=[session['id']]=NEWID

for event_name in sorted(speakers):
  for speaker in speakers[event_name]:
    print "adding Person %s" % speaker['name']
    FOO split speakers['name'] to lastname, firstname
    FOO split speakers['title'] to title, org
    db_session.add(Person(lastname=lastname,firstname=firstname,title=title,org=org,description=speaker['description']))
    FOO associate person with sessions
#  db_session.commit()

