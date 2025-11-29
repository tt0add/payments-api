from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from database.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column()

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    sum: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)