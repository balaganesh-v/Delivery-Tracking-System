from fastapi import Response
from sqlalchemy.orm import Session

from models.driver.drivers import Driver
from repositories.driver_repository import DriverRepository

from utils.security import hash_password, verify_password
from utils.jwt import create_access_token


class DriverService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DriverRepository(db)

    # REGISTER
    def registerDriver(self, data):
        if self.repo.get_driver_by_email(data.email):
            raise ValueError("Driver already exists")
        driver = Driver(
            name=data.name,
            email=data.email,
            phone=data.phone,
            vehicle_number=data.vehicle_number,
            password_hash=hash_password(data.password)
        )
        return self.repo.create_driver(driver)

    # LOGIN
    def loginDriver(self,email: str,password: str,response: Response):
        driver = self.repo.get_driver_by_email(email)
        if not driver or not verify_password(password, driver.password_hash):
            raise ValueError("Invalid credentials")
        token = create_access_token({"driver_id": driver.id})
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return driver, token

    # LOGOUT
    def logoutDriver(self,driver_id: int,response: Response):
        sessions_closed = 0
        active_session = self.repo.get_active_session(self.db, driver_id)
        if active_session:
            self.repo.close_session(self.db, active_session)
            sessions_closed = 1
        response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return {
            "message": "Driver logged out successfully",
            "sessions_closed": sessions_closed
        }

    # CURRENT DRIVER
    def getCurrentLoggedInDriver(self, driver_id: int):
        driver = self.repo.get_driver_by_id(driver_id)
        if not driver:
            raise ValueError("Driver not found")
        return driver

    # LIST OF ORDERS
    def get_orders_for_driver(self, driver_id: int):
        orders = self.repo.get_orders_by_driver_id(driver_id)
        return orders

    # PENDING ORDERS
    def get_pending_orders_for_driver(self, driver_id: int):
        return self.repo.get_pending_orders_by_driver_id(driver_id)
    
    # COMPLETED ORDERS
    def get_completed_orders_for_driver(self, driver_id: int):
        return self.repo.get_completed_orders_by_driver_id(driver_id)
    
    # CHECK-IN
    def check_in_driver(self, driver_id: int, order_id: int):
        if not order_id:
            raise ValueError("order_id is required")

        active = self.repo.get_active_session(driver_id, order_id)
        if active:
            raise ValueError("Already checked in for this order")

        return self.repo.create_session(driver_id, order_id)

    # CHECK-OUT
    def check_out_driver(self, driver_id: int, order_id: int):
        session = self.repo.get_active_session(driver_id, order_id)
        if not session:
            raise ValueError("No active session for this order")

        return self.repo.close_session(session)
