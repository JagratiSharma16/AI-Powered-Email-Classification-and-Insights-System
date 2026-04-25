# db_setup.py

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///emails.db", echo=True)
Base = declarative_base()


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    subject = Column(String(500))
    sender = Column(String(255))
    category = Column(String(100))
    body = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
