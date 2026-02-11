from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models.driver.drivers import Driver
from models.admin.adminAssignAssignments import OrderDriverAssignment
from models.admin.orders import Order
from models.driver.driverOrderSessions import DriverOrderSession


class DriverRepository:
    def __init__(self, db: Session):
        self.db = db

    # -------------------- DRIVER AUTH --------------------

    def get_driver_by_email(self, email: str):
        return self.db.query(Driver).filter(Driver.email == email).first()

    def get_driver_by_id(self, driver_id: int):
        driver = self.db.query(Driver).filter(Driver.id == driver_id).first()
        return ({
            "email" : driver.email,
            "name" : driver.name ,
            "vehicle_number" : driver.vehicle_number,
            "phone" : driver.phone,
            "id" : driver.id
        })

    # -------------------- DRIVER ORDERS --------------------

    def get_orders_by_driver_id(self, driver_id: int):
        results = (
            self.db.query(Order)
            .join(
                OrderDriverAssignment,
                Order.order_id == OrderDriverAssignment.order_id
            )
            .filter(OrderDriverAssignment.driver_id == driver_id)
            .all()
        )

        return [
            {
                "order_id": o.order_id,
                "customer_name": o.customer_name,
                "customer_phone": o.customer_phone,
                "food_name": o.food_name,
                "quantity": o.quantity,
                "price": float(o.price),
                "order_type": o.order_type,
                "delivery_address": o.delivery_address,
                "status": o.status,
                "created_at": o.created_at,
            }
            for o in results
        ]
    
    def get_pending_orders_by_driver_id(self, driver_id: int):
        results = (
            self.db.query(Order)
            .join(
                OrderDriverAssignment,
                Order.order_id == OrderDriverAssignment.order_id
            )
            .filter(
                OrderDriverAssignment.driver_id == driver_id,
                (Order.status == "ASSIGNED") | (Order.status == "PICKED_UP")
            )
            .all()
        )

        return [
            {
                "order_id": o.order_id,
                "customer_name": o.customer_name,
                "customer_phone": o.customer_phone,
                "food_name": o.food_name,
                "quantity": o.quantity,
                "price": float(o.price),
                "order_type": o.order_type,
                "delivery_address": o.delivery_address,
                "status": o.status,
                "created_at": o.created_at,
            }
            for o in results
        ]
    
    def get_completed_orders_by_driver_id(self, driver_id: int):
        
        results = (
            self.db.query(Order)
            .join(
                OrderDriverAssignment,
                Order.order_id == OrderDriverAssignment.order_id
            )
            .filter(
                OrderDriverAssignment.driver_id == driver_id,
                Order.status == "DELIVERED"
            )
            .all()
        )

        return [
            {
                "order_id": o.order_id,
                "customer_name": o.customer_name,
                "customer_phone": o.customer_phone,
                "food_name": o.food_name,
                "quantity": o.quantity,
                "price": float(o.price),
                "order_type": o.order_type,
                "delivery_address": o.delivery_address,
                "status": o.status,
                "created_at": o.created_at,
            }
            for o in results
        ]

        
        results = (
            self.db.query(Order)
            .join(
                OrderDriverAssignment,
                Order.order_id == OrderDriverAssignment.order_id
            )
            .filter(
                OrderDriverAssignment.driver_id == driver_id,
                Order.status == "DELIVERED"
            )
            .all()
        )

        return [
            {
                "order_id": o.order_id,
                "customer_name": o.customer_name,
                "customer_phone": o.customer_phone,
                "food_name": o.food_name,
                "quantity": o.quantity,
                "price": float(o.price),
                "order_type": o.order_type,
                "delivery_address": o.delivery_address,
                "status": o.status,
                "created_at": o.created_at,
            }
            for o in results
        ]

    # -------------------- ACTIVE SESSION --------------------

    def get_active_session(self, driver_id: int, order_id: int):
        session = (
            self.db.query(DriverOrderSession.session_id)
            .filter(
                DriverOrderSession.driver_id == driver_id,
                DriverOrderSession.order_id == order_id,
                DriverOrderSession.check_out_time.is_(None)
            )
            .first()
        )

        return session[0] if session else None

    def get_all_active_sessions(self, driver_id: int):
        return (
            self.db.query(DriverOrderSession)
            .filter(
                DriverOrderSession.driver_id == driver_id,
                DriverOrderSession.check_out_time.is_(None)
            )
            .all()
        )

    # -------------------- CHECK-IN --------------------

    def create_session(self, driver_id: int, order_id: int):
        # Prevent duplicate active session
        existing = self.get_active_session(driver_id, order_id)
        if existing:
            return existing

        order = (
            self.db.query(Order)
            .filter(Order.order_id == order_id)
            .first()
        )
        if not order:
            raise ValueError("Order not found")

        session = DriverOrderSession(
            driver_id=driver_id,
            order_id=order_id,

            # Snapshot (for admin latest updates)
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            food_name=order.food_name,
            quantity=order.quantity,
            price=order.price,
            order_type=order.order_type,
            delivery_address=order.delivery_address,

            order_status="ASSIGNED",
            check_in_time=datetime.now(timezone.utc),
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    # -------------------- CHECK-OUT / DELIVER --------------------

    def close_session(self, session_id: int):
        session = (
            self.db.query(DriverOrderSession)
            .filter(DriverOrderSession.session_id == session_id)
            .first()
        )
        if not session:
            raise ValueError("Session not found")

        if session.check_out_time:
            return session  # already closed

        # Close session
        session.check_out_time = datetime.now(timezone.utc)
        session.order_status = "DELIVERED"

        # Sync order table
        order = (
            self.db.query(Order)
            .filter(Order.order_id == session.order_id)
            .first()
        )
        if order:
            order.status = "DELIVERED"

        self.db.commit()
        self.db.refresh(session)
        return session