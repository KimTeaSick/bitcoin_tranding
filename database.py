from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:$kim99bsd00@nc-db-1.cyu1ow4eutwz.ap-northeast-2.rds.amazonaws.com:3306/nc_bit_trading"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://ipxnms:$kim99bsd00@192.168.10.202:3306/nc_bit_trading"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
        return cls._instance
    
    def get_session(self):
        return self.Session()