from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from database.db import engine

Base = declarative_base()

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    meeting_date = Column(DateTime, default=datetime.utcnow)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    mom = Column(Text, nullable=True)
    customer_insights = Column(Text, nullable=True)
    sentiment = Column(String(255), nullable=True)
    deal_stage = Column(String(255), nullable=True)
    probability = Column(String(50), nullable=True) # Usually string like "75%" or float. We'll use String to be safe.
    
    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")
    followups = relationship("FollowUp", back_populates="meeting", cascade="all, delete-orphan")

class ActionItem(Base):
    __tablename__ = "action_items"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    task = Column(Text, nullable=False)
    owner = Column(String(255), nullable=True)
    due_date = Column(String(255), nullable=True)
    status = Column(String(50), default="Pending")
    
    meeting = relationship("Meeting", back_populates="action_items")

class FollowUp(Base):
    __tablename__ = "followups"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    email_subject = Column(String(255), nullable=True)
    email_body = Column(Text, nullable=True)
    sent = Column(Boolean, default=False)
    
    meeting = relationship("Meeting", back_populates="followups")

# Create tables
def init_db():
    if engine:
        Base.metadata.create_all(bind=engine)
