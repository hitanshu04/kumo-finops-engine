from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from .database import Base
from datetime import datetime

class CloudCost(Base):
    __tablename__ = "cloud_costs"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True)  # e.g., "AWS EC2", "Google Storage"
    amount = Column(Float)                # e.g., 50.00
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_anomaly = Column(Boolean, default=False) # True if the cost is too high