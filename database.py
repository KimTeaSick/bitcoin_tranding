from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Lock

class DatabaseSingleton:
    _instance = None
    _lock = Lock()  # 멀티스레드 환경에서도 안전하게 인스턴스를 보장하기 위한 Lock

    def __new__(cls):
        # Singleton 인스턴스가 없을 때만 생성
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseSingleton, cls).__new__(cls)
                # 데이터베이스 연결 설정
                SQLALCHEMY_DATABASE_URL = "mysql+pymysql://admin:$kim99bsd00@nc-db-1.cyu1ow4eutwz.ap-northeast-2.rds.amazonaws.com:3306/nc_bit_trading"
                cls._instance.engine = create_engine(
                    SQLALCHEMY_DATABASE_URL,
                    pool_pre_ping=True,
                    pool_recycle=3600
                )
                cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
                cls._instance.Base = declarative_base()

            return cls._instance

# DatabaseSingleton을 사용하여 어디서나 같은 인스턴스에 접근
db_instance = DatabaseSingleton()

# 엔진, 세션, 베이스에 접근 가능
engine = db_instance.engine
SessionLocal = db_instance.SessionLocal
Base = db_instance.Base
