import redis
import os

# Get environment variables or use defaults
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
