from pydantic import BaseModel, Field

#TODO : Add fieldValidation

#  Users 
class UserBase(BaseModel):
    username: str = Field(..., min_length=3)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(UserBase):
    password: str

class UserRead(UserBase):
    id: int

#  Books 
class BookBase(BaseModel):
    title: str
    author: str
    price: float = Field(..., ge=0)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = Field(None, ge=0)

class BookRead(BookBase):
    id: int
    owner_id: int
