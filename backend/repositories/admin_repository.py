# repositories/admin_repository.py
from models.admin.adminAssignAssignments import OrderDriverAssignment
from models.admin.admins import Admin
from models.driver.drivers import Driver
from models.admin.orders import Order
from sqlalchemy.orm import Session

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(Admin).filter(Admin.email == email).first()

    def get_by_username(self, username: str):
        return self.db.query(Admin).filter(Admin.username == username).first()

    def create_admin(self, username, email, hashed_password):
        admin = Admin(
            username=username,
            email=email,
            password=hashed_password
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin
    
    def get_all_drivers(self):
        drivers = self.db.query(Driver).all()
        return drivers
    
    def create_driver(self, name, email, phone, vehicle_number, hashed_password):
        driver = Driver(
            name=name,
            email=email,
            phone=phone,
            vehicle_number=vehicle_number,
            password_hash=hashed_password
        )
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        return driver
    
    def get_all_orders(self):
        orders = self.db.query(Order).all()
        return orders
    
    def get_order_by_id(self, order_id):
        return self.db.query(Order).filter(Order.order_id == order_id).first()

    def get_driver_by_id(self, driver_id):
        return self.db.query(Driver).filter(Driver.id == driver_id).first()

    def is_order_assigned(self, order_id):
        return self.db.query(OrderDriverAssignment).filter(OrderDriverAssignment.order_id == order_id).first() is not None

    def create_order_assignment(self, order_id, driver_id):
        assignment = OrderDriverAssignment(order_id=order_id, driver_id=driver_id)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def update_order_status(self, order_id, status):
        order = self.get_order_by_id(order_id)
        order.status = status
        self.db.commit()
        return order

    def get_all_order_assignments(self):
        results = (
            self.db.query(
                OrderDriverAssignment.assignment_id,
                OrderDriverAssignment.order_id,
                OrderDriverAssignment.driver_id,
                OrderDriverAssignment.assigned_at,
                Order.status.label("order_status")
            )
            .join(Order, Order.order_id == OrderDriverAssignment.order_id)
            .all()
        )

        return [
            {
                "assignment_id": r.assignment_id,
                "order_id": r.order_id,
                "driver_id": r.driver_id,
                "assigned_at": r.assigned_at,
                "status": r.order_status   # ✅ delivered or not
            }
            for r in results
        ]
