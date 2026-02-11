from sqlalchemy import Column, Integer, String, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

# Order type enum
class OrderType(str, enum.Enum):
    DELIVERY = "DELIVERY"
    PICKUP = "PICKUP"
    DINE_IN = "DINE_IN"

# Order status enum
class OrderStatus(str, enum.Enum):
    PLACED = "PLACED"
    ASSIGNED = "ASSIGNED"
    DELIVERED = "DELIVERED"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(15), nullable=False)
    food_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    delivery_address = Column(String(255))
    status = Column(Enum(OrderStatus), default=OrderStatus.PLACED)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # One order → many driver sessions (history)
    sessions = relationship(
        "DriverOrderSession",
        back_populates="order"
    )
    
