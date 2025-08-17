from sqlalchemy import select, insert, update, delete
from .database import engine
from .tables import users, books

#  Users 
def create_user(user_data: dict):
    with engine.begin() as conn:
        result = conn.execute(insert(users).values(**user_data))
    return result.inserted_primary_key[0]  


def get_user_by_username(username: str):
    with engine.connect() as conn:
        result = conn.execute(select(users).where(users.c.username == username)).mappings().first()
        return dict(result) if result else None

#  Books 
def create_book(owner_id,book_data: dict):
    with engine.begin() as conn:
        conn.execute(insert(books).values(**book_data,owner_id=owner_id))

def get_books(filters: dict = None, max_price: float | None = None, min_price: float | None = None, limit: int = 10, offset: int = 0):
    query = select(books)
    if filters:
        for col, val in filters.items():
            query = query.where(getattr(books.c, col).ilike(f"%{val}%"))
    if max_price is not None:
        query = query.where(books.c.price <= max_price)
    if min_price is not None:
        query = query.where(books.c.price >= min_price) 
    query = query.limit(limit).offset(offset)
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(query).mappings().all()]

def get_book_by_id(book_id: int):
    with engine.connect() as conn:
        result = conn.execute(select(books).where(books.c.id == book_id)).mappings().first()
        return dict(result) if result else None

def update_book(book_id: int, updates: dict):
    with engine.begin() as conn:
        conn.execute(update(books).where(books.c.id == book_id).values(**updates))

def delete_book(book_id: int):
    with engine.begin() as conn:
        conn.execute(delete(books).where(books.c.id == book_id))
