from fastapi import APIRouter, Depends, HTTPException , Response
from sqlalchemy.orm import Session
from database import get_db
from services.admin_service import AdminService
from repositories.admin_repository import AdminRepository
from schemas.admin import AdminLogin, AdminOTPVerify, AdminRegister , AddNewDriver
from schemas.order import AssignDriver

from utils.jwt import create_access_token
from dependencies.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/register")
def register_admin(data: AdminRegister, db: Session = Depends(get_db)):
    service = AdminService(AdminRepository(db))
    admin = service.admin_register(data.username, data.email, data.password)
    if not admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {
        "message": "Admin registered successfully. Confirmation email sent.",
        "admin_id": admin.id,
        "email": admin.email
    }

@router.post("/login")
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):
    service = AdminService(AdminRepository(db))
    admin = service.admin_login(data.email, data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "admin_id": admin.id,
        "message": "OTP sent to email. Please verify."
    }

@router.post("/verify-otp")
def verify_otp(data: AdminOTPVerify,response:Response, db: Session = Depends(get_db)):
    service = AdminService(AdminRepository(db))
    admin = service.verify_otp(data.email, data.otp)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    # Generate JWT token with admin details
    token = create_access_token({
        "email": admin.email,
        "admin_id": admin.id
    })
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,     # prevents JS access
        secure=True,       # only over HTTPS
        samesite="Lax"     # prevents CSRF
    )
    return {
        "message": "OTP verified successfully.User Logged in Successfully❤️!!",
        "token": token,
        "admin_id": admin.id,
    }

@router.get("/drivers")
def get_all_drivers(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    service = AdminService(AdminRepository(db))
    drivers = service.get_all_drivers()
    return {"drivers": drivers, "accessed_by": current_admin["email"]}

@router.post("/add-new-driver")
def add_new_driver(data: AddNewDriver, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    service = AdminService(AdminRepository(db))
    driver = service.add_new_driver(data.name, data.email, data.phone, data.vehicle_number, data.password)
    return {
        "message": "Driver added successfully. Credentials emailed.",
        "driver_id": driver.id,
        "email": driver.email,
        "added_by": current_admin["email"]
    }
    
@router.get("/orders")
def get_all_orders(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    service = AdminService(AdminRepository(db))
    orders = service.get_all_orders()
    return {"orders": orders, "accessed_by": current_admin["email"]}

@router.post("/assign-order")
def assign_order(data: AssignDriver, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    service = AdminService(AdminRepository(db))
    assignment, error = service.assign_order_to_driver(data.order_id, data.driver_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "message": "Order assigned successfully",
        "order_id": assignment.order_id,
        "driver_id": assignment.driver_id,
        "assigned_by": current_admin["email"]
    }
    
@router.get("/ordered-assignments")
def fetch_ordered_assignments(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    service = AdminService(AdminRepository(db))
    assignments = service.get_ordered_assignments()
    return {
        "assignments": assignments,
        "accessed_by": current_admin["email"]
    }
    
