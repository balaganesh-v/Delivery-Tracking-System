from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from database import Base

class DriverLocation(Base):
    __tablename__ = "driver_location"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
