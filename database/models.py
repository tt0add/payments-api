from sqlalchemy import Column, Integer, DateTime
from database.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    balance = Column(Integer)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sum = Column(Integer)
    datetime = Column(DateTime, default=datetime.utcnow)