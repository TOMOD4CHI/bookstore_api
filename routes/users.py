from fastapi import APIRouter, HTTPException
from ..models import UserCreate, UserLogin, UserRead
from ..crud import create_user, get_user_by_username
from ..auth import hash_password, verify_password, create_access_token,create_long_access_token

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate):
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_pw = hash_password(user.password)
    return {"id": create_user({"username": user.username, "password_hash": hashed_pw}), "username": user.username}

@router.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["id"], "username": db_user["username"]})
    # Create a long access token for extended sessions
    # won't be used for now until i implement a logout feature to revoke it
    # tho it can be used as a token extender but the token will persist and should be deleted after the expiration time
    # long_token = create_long_access_token({"sub": db_user["id"], "username": db_user["username"]})
    return {"access_token": token, "token_type": "bearer"}
