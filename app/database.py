from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
import datetime

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ClientRequestHistory(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, index=True)
    email = Column(String, index=True)
    uuid = Column(String, index=True)
    report_name = Column(String, index=True)
    inn = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)