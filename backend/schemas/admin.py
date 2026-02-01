# schemas/admin_schema.py
from pydantic import BaseModel, EmailStr

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminOTPVerify(BaseModel):
    email: EmailStr
    otp: str

# New schema for registration
class AdminRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class AddNewDriver(BaseModel):
    name: str
    email: EmailStr
    phone: str
    vehicle_number: str
    password: str