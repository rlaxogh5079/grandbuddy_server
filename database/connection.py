from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import urllib.parse
import os
import logging

logging.basicConfig(level=logging.ERROR)

class DBObject:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        db_config = self._get_db_config()
        db_url = self._build_db_url(**db_config)
        
        try:
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            logging.error(f"데이터베이스 연결 오류: {e}")
            raise RuntimeError("데이터베이스 연결에 실패했습니다. 환경 변수를 확인하세요.") from e

    @staticmethod
    def _get_db_config():
        db_config = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "name": os.getenv("DB_NAME"),
        }
        
        if None in db_config.values():
            missing_keys = [k for k, v in db_config.items() if v is None]
            raise RuntimeError(f"환경 변수 누락: {', '.join(missing_keys)}. .env 파일을 확인하세요.")
        
        return db_config

    @staticmethod
    def _build_db_url(user, password, host, port, name):
        return (
            f"mysql+pymysql://{urllib.parse.quote_plus(user)}:"
            f"{urllib.parse.quote_plus(password)}@{host}:{port}/"
            f"{urllib.parse.quote_plus(name)}"
        )

    def get_session(self):
        return self.Session()

    @contextmanager
    def session_scope(self):
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"SQL 오류 발생: {e}")
            raise
        finally:
            session.close()
