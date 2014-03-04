from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

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
assoc_event_sponsor = Table('assoc_event_sponsor', Base.metadata,
  Column('event_id', Integer, ForeignKey('event.id')),
  Column('sponsor_id', Integer, ForeignKey('sponsor.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)

# a conference sponsor entity, which is not tied to a particular event
class Sponsor(Base):
  __tablename__ = 'sponsor'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(63))
  url = Column(String(255))
  event = relationship('Event', secondary=assoc_event_sponsor, backref='sponsor')

  def __init__(self, name=None, url=None):
    self.name=name
    self.url=url

  def __repr__(self):
    return '<Sponsor %r>' % (self.name)

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
#  session = relationship('Session',backref='person',secondary='assoc_person_session')

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

# an event (for us they are just labelled by year, e.g. 2013, 2014)
class Event(Base):
  __tablename__ = 'event'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True)
  timeslot = relationship('Timeslot', backref='event')

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

