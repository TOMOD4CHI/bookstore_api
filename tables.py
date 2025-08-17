from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey,DateTime
from .database import metadata

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String, unique=True, nullable=False),
    Column("password_hash", String, nullable=False)
)

books = Table(
    "books", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("price", Float, nullable=False),
    Column("owner_id", Integer, ForeignKey("users.id"))
)
# This table is for storing refresh tokens
# For now it won't be used because we don't have a continuous refresh token strategy
# No logout  to trigger the deletion of expired tokens
# This token works when the short-lived access token expires so the user send a silent POST /refresh to refresh the access token 
# and potentially the refresh token
refresh_tokens = Table(
    "refresh_tokens", metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False)
)
