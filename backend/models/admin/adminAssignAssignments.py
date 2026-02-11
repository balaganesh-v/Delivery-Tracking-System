from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database import Base

class OrderDriverAssignment(Base):
    __tablename__ = "order_driver_assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, unique=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    assigned_at = Column(TIMESTAMP, server_default=func.now())
