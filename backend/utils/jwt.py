import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_HOURS = 24  # Token expires in 24 hours
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate JWT token with expiration
    
    Args:
        data: Payload data to encode
        expires_delta: Custom expiration time (default: 24 hours)
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str):
    """Decode and verify JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        dict: Decoded payload if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
