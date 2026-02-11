from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class DriverCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    vehicle_number: str
    password: str


class DriverLogin(BaseModel):
    email: EmailStr
    password: str


class DriverResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    vehicle_number: str
    
class CheckInRequest(BaseModel):
    order_id: int

class CheckOutRequest(BaseModel):
    order_id: int

    model_config = ConfigDict(from_attributes=True)
