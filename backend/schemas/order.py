from pydantic import BaseModel
from typing import Optional
from models.admin.orders import OrderType, OrderStatus
from pydantic import ConfigDict

# Create order
class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    food_name: str
    quantity: int
    price: float
    order_type: OrderType
    delivery_address: Optional[str] = None

# Assign driver
class AssignDriver(BaseModel):
    order_id: int
    driver_id: int
    
# Response schema
class OrderResponse(BaseModel):
    order_id: int
    customer_name: str
    food_name: str
    quantity: int
    price: float
    order_type: OrderType
    delivery_address: Optional[str]
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)


