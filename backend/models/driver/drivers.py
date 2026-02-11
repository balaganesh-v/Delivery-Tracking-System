from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    vehicle_number = Column(String(50))
    password_hash = Column(String(255), nullable=False)

    # One driver → many order sessions
    sessions = relationship(
        "DriverOrderSession",
        back_populates="driver",
        cascade="all, delete-orphan"
    )
