from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

# a conference sponsor entity, which is not tied to a particular event
class Sponsor(Base):
  __tablename__ = 'sponsors'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(63))
  url = Column(String(255))

  def __init__(self, name=None, url=None):
    self.name=name
    self.url=url

  def __repr__(self):
    return '<Sponsor %r>' % (self.name)

# a person, could be any person, speaker or team member
class Person(Base):
  __tablename__ = 'persons'
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

# an event (for us they are just labelled by year, e.g. 2013, 2014)
class Event(Base):
  __tablename__ = 'events'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True)
  timeslots = relationship('Timeslot', backref='events')

  def __init__(self, name=None):
    self.name=name

  def __repr__(self):
    return '<Event %r>' % (self.name)

# a time slot in the program schedule which may contain one or multiple sessions
class Timeslot(Base):
  __tablename__ = 'timeslots'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  time_start = Column(DateTime())
  time_end = Column(DateTime())
  event_id = Column(Integer, ForeignKey('events.id'))
  sessions = relationship('Session', backref='timeslots')

  def __init__(self, time_start=None, time_end=None, event_id=None):
    self.time_start=time_start
    self.time_end=time_end
    self.event_id=event_id

  def __repr__(self):
    return '<Timeslot %r>' % (self.name)

# conference session (e.g. Lunch, Registration,
# Keynote, Breakout Session 1, Workshop 4, etc.)
class Session(Base):
  __tablename__ = 'sessions'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  description = Column(String(4095))
  location = Column(String(255))
  timeslot_id = Column(Integer, ForeignKey('timeslots.id'))

  def __init__(self, name=None, description=None, location=None, timeslot_id=None):
    self.name=name
    self.description=description
    self.location=location
    self.timeslot_id=timeslot_id

  def __repr__(self):
    return '<Session %r>' % (self.name)

# enumerates the possible team names (e.g. Marketing Team, Content Team)
class Team(Base):
  __tablename__ = 'teams'
  __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  event_id = Column(Integer, ForeignKey('events.id'))

  def __init__(self, name=None, event_id=None):
    self.name=name
    self.event_id=event_id

  def __repr__(self):
    return '<Team %r>' % (self.name)

# thought about making sessions<->timeslots many-to-many
# (one session could appear in multiple timeslots
# but decided against it since it hasn't happened in the first 5
# years of the summit and it complicates management
# so using the usual one-to-many technique of foreign key and backref
# assoc_sessions_timeslots = Table('assoc_sessions_timeslots', Base.metadata,
#   Column('session_id', Integer, ForeignKey('sessions.id')),
#   Column('timeslot_id', Integer, ForeignKey('timeslots.id')),
#   mysql_engine='InnoDB',
#   mysql_charset='utf8',
# )

# person can appear in multiple sessions,
# and session has multiple persons as  participants
assoc_persons_sessions = Table('assoc_persons_sessions', Base.metadata,
  Column('person_id', Integer, ForeignKey('persons.id')),
  Column('session_id', Integer, ForeignKey('sessions.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)

# person can also appear on multiple organizing teams,
# and organizing team has multiple persons as members
assoc_persons_teams = Table('assoc_persons_teams', Base.metadata,
  Column('person_id', Integer, ForeignKey('persons.id')),
  Column('team_id', Integer, ForeignKey('teams.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)

# sponsor can appear on multiple events,
# and events have multiple sponsors
assoc_events_sponsors = Table('assoc_events_sponsors', Base.metadata,
  Column('event_id', Integer, ForeignKey('events.id')),
  Column('sponsor_id', Integer, ForeignKey('sponsors.id')),
  mysql_engine='InnoDB',
  mysql_charset='utf8',
)
