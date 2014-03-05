from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, subqueryload
from sqlalchemy.ext.declarative import declarative_base
import string

from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import Pool

db_server = 'sql.mit.edu'
db_username = 'sustainability'
# keep database password off github
with open('.dbpassword') as fp:
  db_password = string.strip(fp.read())
db_name = 'sustainability+summit'

db_url = "mysql://%s:%s@%s/%s?charset=utf8&use_unicode=1" % (db_username, db_password, db_server, db_name)
db_engine = create_engine(db_url, convert_unicode=True, pool_size=10, pool_recycle=30)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))
Base = declarative_base()
Base.query = db_session.query_property()

@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
  cursor = dbapi_connection.cursor()
  try:
    cursor.execute("SELECT 1")
  except:
    connection_proxy._pool.dispose()
    raise exc.DisconnectionError()
  cursor.close()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=db_engine)
