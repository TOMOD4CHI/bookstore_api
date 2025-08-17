from fastapi import FastAPI
from .database import metadata, engine
from .tables import users, books
from .routes import users as user_routes, books as book_routes

metadata.create_all(engine)

app = FastAPI()

app.include_router(user_routes.router, tags=["Users"])
app.include_router(book_routes.router, tags=["Books"])
