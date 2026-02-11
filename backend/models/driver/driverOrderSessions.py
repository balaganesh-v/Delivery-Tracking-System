from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
    Enum, Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class DriverOrderSession(Base):
    __tablename__ = "driver_order_sessions"

    session_id = Column(Integer, primary_key=True, index=True)

    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)

    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(15), nullable=False)
    food_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    order_type = Column(
        Enum("DELIVERY", "PICKUP", "DINE_IN", name="order_type_enum"),
        nullable=False
    )

    delivery_address = Column(String(255))

    order_status = Column(
        Enum("ASSIGNED", "DELIVERED", name="order_status_enum"),
        default="ASSIGNED",
        nullable=False
    )

    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime)

    created_at = Column(DateTime, server_default=func.now())

    # ✅ REQUIRED relationship
    driver = relationship(
        "Driver",
        back_populates="sessions"
    )
    order = relationship(
        "Order",
        back_populates="sessions"
    )