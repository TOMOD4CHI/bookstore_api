import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost", decode_responses=True)

async def cache_invalidation(owner_id: int):
    cache_key = f"user:{owner_id}:books"
    await redis_client.delete(cache_key)