from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base
import datetime, time, os, io
from subprocess import call

# person can appear in multiple sessions,
# and session has multiple persons as  participants
assoc_person_session = Table('assoc_person_session', Base.metadata,
  Column('person_id', Integer, ForeignKey('person.id')),
  Column('session_id', Integer, ForeignKey('session.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)

# person can also appear on multiple organizing teams,
# and organizing team has multiple persons as members
assoc_person_team = Table('assoc_person_team', Base.metadata,
  Column('person_id', Integer, ForeignKey('person.id')),
  Column('team_id', Integer, ForeignKey('team.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)

# sponsor can appear on multiple events,
# and events have multiple sponsors
assoc_sponsor_sponsorship = Table('assoc_sponsor_sponsorship', Base.metadata,
  Column('sponsor_id', Integer, ForeignKey('sponsor.id')),
  Column('sponsorship_id', Integer, ForeignKey('sponsorship.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)

#assoc_event_sponsorship = Table('assoc_event_sponsorship', Base.metadata,
#  Column('event_id', Integer, ForeignKey('event.id')),
#  Column('sponsorship_id', Integer, ForeignKey('sponsorship.id')),
#  mysql_engine='InnoDB',
#  mysql_charset='utf8',
#)

class Sponsorship(Base):
  __tablename__ = 'sponsorship'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  event_id = Column(Integer, ForeignKey('event.id'))
  name = Column(String(255))
  priority = Column(Integer)
  sponsor = relationship('Sponsor', secondary=assoc_sponsor_sponsorship, backref='sponsorship')

  def __init__(self, name=None, priority=0, event_id=None):
    self.name=name
    self.priority=priority
    self.event_id=event_id

  def __repr__(self):
    return '<Sponsorship %r>' % (self.event_id + ' ' + self.name)

# a conference sponsor entity, which is not tied to a particular event
class Sponsor(Base):
  __tablename__ = 'sponsor'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(63))
  url = Column(String(255))

  def __init__(self, name=None, url=None):
    self.name=name
    self.url=url

  def __repr__(self):
    return '<Sponsor %r>' % (self.name)

  def get_logo_svg_url(self):

    # the source image we are looking for
    src_filename = 'summit/media/db-sponsor/'+str(self.id)

    # where we hope to find a cached copy, or create one if it doesn't exist
    cache_url = '/static/cache/sponsor_%s.svg' % str(self.id)
    dest_filename = 'summit'+cache_url

    if not os.path.exists(src_filename):
      return None

    if not os.path.exists(dest_filename):
      call(["cp", src_filename, dest_filename])

    return cache_url



# a person, could be any person, speaker or team member
class Person(Base):
  __tablename__ = 'person'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  lastname = Column(String(63))
  firstname = Column(String(63))
  org = Column(String(255))
  title = Column(String(255))
  org2 = Column(String(255))
  title2 = Column(String(255))
  description = Column(String(4095))

  def __init__(self, lastname=None, firstname=None, org=None, title=None, org2=None, title2=None, description=None):
    self.lastname = lastname
    self.firstname = firstname
    self.org = org
    self.title = title
    self.org2 = org2
    self.title2 = title2
    self.description = description

  def __repr__(self):
    return '<Person %r>' % (self.firstname + " " + self.lastname)

  def get_picture_url(self,size='120x120'):

    # the source image we are looking for
    src_filename = 'summit/media/db-person/'+str(self.id)

    # where we hope to find a cached copy, or create one if it doesn't exist
    cache_url = '/static/cache/person_%s_%s.jpg' % (str(self.id), size)
    dest_filename = 'summit'+cache_url

    if not os.path.exists(src_filename):
      return '/static/images/blank.gif'

    if not os.path.exists(dest_filename):
      call(["convert", "-sharpen", "0x0.8", "-strip", src_filename, "-thumbnail", size+"^", "-gravity", "center", "-extent", size, "-quality", "90", dest_filename])

    return cache_url


# an event (for us they are just labelled by year, e.g. 2013, 2014)
class Event(Base):
  __tablename__ = 'event'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True)
  timeslot = relationship('Timeslot', backref='event')
  sponsorship = relationship('Sponsorship', backref='event')
  team = relationship('Team', backref='event')

  def __init__(self, name=None):
    self.name=name

  def __repr__(self):
    return '<Event %r>' % (self.name)

# a time slot in the program schedule which may contain one or multiple sessions
class Timeslot(Base):
  __tablename__ = 'timeslot'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  time_start = Column(DateTime())
  time_end = Column(DateTime())
  event_id = Column(Integer, ForeignKey('event.id'))
  session = relationship('Session', backref='timeslot')

  def __init__(self, time_start=None, time_end=None, event_id=None):
    self.time_start=time_start
    self.time_end=time_end
    self.event_id=event_id

  def __repr__(self):
    return '<Timeslot %r>' % (self.event_id + ' ' + self.time_start)

# conference session (e.g. Lunch, Registration,
# Keynote, Breakout Session 1, Workshop 4, etc.)
class Session(Base):
  __tablename__ = 'session'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  description = Column(String(4095))
  location = Column(String(255))
  timeslot_id = Column(Integer, ForeignKey('timeslot.id'))
  person = relationship('Person', secondary=assoc_person_session, backref='session')

  def __init__(self, name=None, description=None, location=None, timeslot_id=None):
    self.name=name
    self.description=description
    self.location=location
    self.timeslot_id=timeslot_id

  def __repr__(self):
    return '<Session %r>' % (self.name)

# enumerates the possible team names (e.g. Marketing Team, Content Team)
class Team(Base):
  __tablename__ = 'team'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  event_id = Column(Integer, ForeignKey('event.id'))
  person = relationship('Person', secondary=assoc_person_team, backref='team')

  def __init__(self, name=None, event_id=None):
    self.name=name
    self.event_id=event_id

  def __repr__(self):
    return '<Team %r>' % (self.name)

