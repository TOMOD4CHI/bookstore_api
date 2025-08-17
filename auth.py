import jwt
import os
from passlib.hash import bcrypt
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
# LONG_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

"""
def create_long_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=LONG_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
"""
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
