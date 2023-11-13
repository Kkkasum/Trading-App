from sqlalchemy import Column, String, Integer

from src.db import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    message = Column(String)
