from sqlalchemy.orm import Session

from models.admin.admins import Admin
from models.driver.drivers import Driver
from models.admin.orders import Order
from models.admin.adminAssignAssignments import OrderDriverAssignment
from models.driver.driverOrderSessions import DriverOrderSession


class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # ADMIN
    # =========================================================

    def get_by_email(self, email: str):
        return self.db.query(Admin).filter(Admin.email == email).first()

    def get_by_username(self, username: str):
        return self.db.query(Admin).filter(Admin.username == username).first()

    def create_admin(self, username: str, email: str, hashed_password: str):
        admin = Admin(
            username=username,
            email=email,
            password=hashed_password,
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    # =========================================================
    # DRIVERS
    # =========================================================

    def get_all_drivers(self):
        return self.db.query(Driver).all()

    def get_driver_by_id(self, driver_id: int):
        return self.db.query(Driver).filter(Driver.id == driver_id).first()

    def create_driver(
        self,
        name: str,
        email: str,
        phone: str,
        vehicle_number: str,
        hashed_password: str,
    ):
        driver = Driver(
            name=name,
            email=email,
            phone=phone,
            vehicle_number=vehicle_number,
            password_hash=hashed_password,
        )
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        return driver

    # =========================================================
    # ORDERS
    # =========================================================

    def get_all_orders(self):
        return self.db.query(Order).all()

    def get_order_by_id(self, order_id: int):
        return self.db.query(Order).filter(Order.order_id == order_id).first()

    def update_order_status(self, order_id: int, status: str):
        order = self.get_order_by_id(order_id)
        if order:
            order.status = status
            self.db.commit()
        return order

    # =========================================================
    # ASSIGNMENTS
    # =========================================================

    def is_order_assigned(self, order_id: int) -> bool:
        return (
            self.db.query(OrderDriverAssignment)
            .filter(OrderDriverAssignment.order_id == order_id)
            .first()
            is not None
        )

    def create_order_assignment(self, order_id: int, driver_id: int):
        assignment = OrderDriverAssignment(
            order_id=order_id,
            driver_id=driver_id,
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    
    # ORDERS THAT ARE NOT ASSIGNED TO ANY DRIVER
    def get_available_orders(self):
        subquery = self.db.query(OrderDriverAssignment.order_id).subquery()
        return self.db.query(Order).filter(~Order.order_id.in_(subquery)).all()
    
    # GET ALL ASSIGNMENTS IN DESCENDING ORDER OF ASSIGNMENT TIME
    def get_all_order_assignments(self):
        results = (
            self.db.query(
                OrderDriverAssignment.assignment_id,
                OrderDriverAssignment.assigned_at,

                Order.order_id,
                Order.food_name,
                Order.quantity,
                Order.price,
                Order.status.label("order_status"),
                Order.customer_name,
                Order.customer_phone,
                Order.delivery_address,

                Driver.id.label("driver_id"),
                Driver.name.label("driver_name"),
                Driver.phone.label("driver_phone"),
                Driver.vehicle_number,
            )
            .join(Order, Order.order_id == OrderDriverAssignment.order_id)
            .join(Driver, Driver.id == OrderDriverAssignment.driver_id)
            .order_by(OrderDriverAssignment.assigned_at.desc())
            .all()
        )

        return [
            {
                "assignment_id": r.assignment_id,
                "assigned_at": r.assigned_at,

                "order_id": r.order_id,
                "food_name": r.food_name,
                "quantity": r.quantity,
                "price": float(r.price),
                "order_status": r.order_status,
                "customer_name": r.customer_name,
                "customer_phone": r.customer_phone,
                "delivery_address": r.delivery_address,

                "driver_id": r.driver_id,
                "driver_name": r.driver_name,
                "driver_phone": r.driver_phone,
                "vehicle_number": r.vehicle_number,
            }
            for r in results
        ]

    # =========================================================
    # LATEST UPDATES (ADMIN DASHBOARD)
    # =========================================================

    def get_latest_updates(self):
        return (
            self.db.query(DriverOrderSession)
            .order_by(DriverOrderSession.session_id.desc())
            .all()
        )