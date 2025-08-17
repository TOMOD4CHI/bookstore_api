from fastapi import APIRouter, Depends, HTTPException, Query,status
from fastapi.security import OAuth2PasswordBearer
from ..models import BookCreate, BookUpdate, BookRead
from ..crud import create_book, get_books, get_book_by_id, update_book, delete_book
from ..auth import decode_access_token
from ..tables import books as books_table, users as users_table
import json
from ..cache import redis_client , cache_invalidation

#To test this use the thunder client vscode extension with the following HTTP header
# Authorization: Bearer <your_token>

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        username = payload.get("username")
        id = payload.get("sub")
        if username is None or id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"id": id, "username": username}


@router.get("/me")
def who_am_i(current_user: dict = Depends(get_current_user)):
    return {"id": current_user["id"], "username": current_user["username"]}

# Caching with redis for better performance and scalability

"""
@router.get("/books/my", response_model=list[BookRead])
async def get_my_books_with_caching(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    cache_key = f"user:{user_id}:books"
    cache = await redis_client.get(cache_key)
    if cache:
        return json.loads(cache)
    books = get_books(filters={"owner_id": user_id})
    await redis_client.set(cache_key, json.dumps(books), ex=60*5)
    return books
"""
@router.get("/books/my")
async def get_my_books(current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    return get_books(filters={"owner_id": user_id})

@router.get("/books", response_model=list[BookRead])
def list_books(
    title: str | None = None,
    author: str | None = None,
    max_price: float | None = None,
    min_price: float | None = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    filters = {}
    if title:
        filters["title"] = title
    if author:
        filters["author"] = author
    return get_books(filters, max_price, min_price, limit, offset)

@router.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# The cache invalidation function is called after modifying the data so the db and cache are in sync

@router.post("/books", response_model=BookRead)
def add_book(book: BookCreate, current_user: dict = Depends(get_current_user)):
    create_book(current_user["id"], book.model_dump())
    #cache_invalidation(current_user["id"])
    return book

@router.put("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookUpdate, current_user: dict = Depends(get_current_user)):
    existing_book = get_book_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if existing_book["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this book")
    update_book(book_id, book.model_dump())
    #cache_invalidation(current_user["id"])
    return book

@router.delete("/books/{book_id}", response_model=BookRead)
def delete_book(book_id: int, current_user: dict = Depends(get_current_user)):
    existing_book = get_book_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if existing_book["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this book")
    delete_book(book_id)
    #cache_invalidation(current_user["id"])
    return existing_book
