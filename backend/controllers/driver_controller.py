from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from services.driver_service import DriverService
from schemas.driver import DriverCreate, DriverLogin , CheckInRequest , CheckOutRequest
from dependencies.auth import get_current_driver
from database import get_db

router = APIRouter(prefix="/drivers", tags=["Driver Management"])


""" DRIVER AUTHENTICATION AND PROFILE """
# REGISTER
@router.post("/register")
def register(data: DriverCreate, db: Session = Depends(get_db)):
    try:
        service = DriverService(db)
        return service.registerDriver(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# LOGIN
@router.post("/login")
def login(data: DriverLogin, response: Response, db: Session = Depends(get_db)):
    try:
        service = DriverService(db)
        driver, token = service.loginDriver(
            email=data.email,
            password=data.password,
            response=response
        )
        return {
            "driver_id": driver.id,
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# LOGOUT
@router.post("/logout")
def logout(response: Response,driver_id: int = Depends(get_current_driver),db: Session = Depends(get_db)):
    try:
        service = DriverService(db)
        return service.logoutDriver(driver_id, response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



""" PROFILE """
# PROFILE INFO
@router.get("/me")
def get_current_driver_info(driver_id: int = Depends(get_current_driver),db: Session = Depends(get_db)):
    try:
        service = DriverService(db)
        return service.getCurrentLoggedInDriver(driver_id)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))




""" ORDERS """
# ASSIGNED ORDERS
@router.get("/assigned-orders")
def get_driver_orders(driver_id:
    int = Depends(get_current_driver),db: Session = Depends(get_db)):
    service = DriverService(db)
    orders = service.get_orders_for_driver(driver_id)
    return {"orders": orders}

# PENDING ORDERS
@router.get("/pending-orders")
def pending_orders(driver_id: int = Depends(get_current_driver), db: Session = Depends(get_db)):
    service = DriverService(db)
    orders = service.get_pending_orders_for_driver(driver_id)
    return {"pending_orders": orders}

# COMPLETED ORDERS
@router.get("/completed-orders")
def completed_orders(driver_id: int = Depends(get_current_driver), db: Session = Depends(get_db)):
    service = DriverService(db)
    orders = service.get_completed_orders_for_driver(driver_id)
    return {"completed_orders": orders}




""" DRIVER SESSIONS """
# CHECK-IN || START TO DELIVERY THE ORDER
@router.post("/check-in")
def check_in(
    data: CheckInRequest,
    driver_id: int = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    service = DriverService(db)
    session = service.check_in_driver(driver_id, data.order_id)
    return {
        "message": "Check-in successful",
        "session_id": session.id,
        "check_in_time": session.check_in_time
    }

# CHECK-OUT || COMPLETE THE DELIVERY
@router.post("/check-out")
def check_out(
    data: CheckOutRequest,
    driver_id: int = Depends(get_current_driver),
    db: Session = Depends(get_db)
):
    service = DriverService(db)
    session = service.check_out_driver(driver_id, data.order_id)
    return {
        "message": "Check-out successful",
        "check_out_time": session.check_out_time
    }
