# one-time script to import the old JSON data into new model

from summit.database import db_session
from summit.models import *
import json
import re

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

team_json=open('/mit/summit/data/team.json').read();
team=json.loads(team_json);

session_id_conv={}

for event_name in sorted(team):
  e=Event.query.filter(Event.name == event_name).first()
  print e.id
  t = Team(name='',event_id=e.id)
  db_session.add(t)
  db_session.commit()
  for item in team[event_name]:
    if 'group_name' not in item:
      firstname, lastname = item['name'].rsplit(' ',1)
      print "... adding Person %s, %s" % (lastname, firstname)
      if 'bio' in item:
        description = item['bio']
      else:
        description=''
      if 'title' in item:
        title = item['title']
      else:
        title = ''
      p = Person(lastname=lastname,firstname=firstname,title=title,org='MIT Sustainability Summit',description=description)
      db_session.add(p)
      db_session.commit()
      t.person.append(p);
      db_session.add(p)
      db_session.commit()
    else:
      print item['group_name']
      t2 = Team(name=item['group_name'],event_id=e.id)
      db_session.add(t2)
      db_session.commit()
      print t.id
      for item2 in item['group_members']:
        firstname, lastname = item2['name'].rsplit(' ',1)
        if 'bio' in item2:
          description = item2['bio']
        else:
          description=''
        print "... adding Person %s, %s | %s, %s" % (lastname, firstname, t2.name, 'MIT Sustainability Summit')
        p = Person(lastname=lastname,firstname=firstname,title=t.name,org='MIT Sustainability Summit',description=description)
        db_session.add(p)
        db_session.commit()
        t2.person.append(p);
        db_session.add(p)
        db_session.commit()

#    p = Person(lastname=lastname,firstname=firstname,title=title,org=org,description=description)
#    try:
#    session_id_conv[event_name+'/'+speaker['session']].person.append(p);
#    except:
#      print('error adding person to session')
#    db_session.add(p);
#    db_session.commit()
#    last_person = Person.query.filter(Person.lastname==lastname and Person.firstname==firstname).first()

#    FOO associate person with sessions

