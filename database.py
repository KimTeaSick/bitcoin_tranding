from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://ipxnms:$kim99bsd00@192.168.10.202:3306/nc_bit_trading"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
