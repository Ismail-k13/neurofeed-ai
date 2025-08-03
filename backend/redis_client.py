import redis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to Redis using environment variables
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def test_connection():
    try:
        pong = r.ping()
        print("✅ Redis Connected:", pong)
    except Exception as e:
        print("❌ Redis Error:", e)

if __name__ == "__main__":
    test_connection()
