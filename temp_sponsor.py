# one-time script to import the old JSON data into new model

from summit.database import db_session
from summit.models import *
import json
import re
import datetime, time, os
from subprocess import call

#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

data_json=open('/mit/summit/data/sponsors.json').read();
data=json.loads(data_json);

session_id_conv={}


for event_name in sorted(data):
  i=0
  e=Event.query.filter(Event.name == event_name).first()
  for sponsorship in data[event_name]:
    s = Sponsorship(name=sponsorship['level'], priority=i, event_id=e.id)
    db_session.add(s)
    db_session.commit()
    for sponsor in sponsorship['sponsors']:
      s2 = Sponsor(name=sponsor['name'], url=sponsor['url'])
      db_session.add(s2)
      s.sponsor.append(s2)
      db_session.commit()
      
      call(["cp","/mit/summit/images/sponsors/"+str(sponsor['id'])+".png","summit/media/db-sponsor/%s.png" % str(s2.id)])
      call(["cp","/mit/summit/images/sponsors/"+str(sponsor['id'])+".svg","summit/media/db-sponsor/%s.svg" % str(s2.id)])
      
    i=i+1

