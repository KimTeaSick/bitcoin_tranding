from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://ipxnms:$kim99bsd00@192.168.10.202:3306/nc_bit_trading"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://ipxnms:$kim99bsd00@121.165.242.171:33062/nc_bit_trading"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:$kim99bsd00@nc-db-1.cyu1ow4eutwz.ap-northeast-2.rds.amazonaws.com:3306/nc_bit_trading"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@event.listens_for(engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # this parameter is always False as of SQLAlchemy 2.0,
        # but is still accepted by the event hook.  In 1.x versions
        # of SQLAlchemy, "branched" connections should be skipped.
        return

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select(1))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select(1))
        else:
            raise

Base = declarative_base()
