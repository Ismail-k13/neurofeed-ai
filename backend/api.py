from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import redis
import struct
from redis.commands.search.query import Query as RedisQuery

app = FastAPI()

# Optional: Enable CORS if frontend is used
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis and model setup
r = redis.Redis(host="localhost", port=6379, decode_responses=False)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Utility: Convert float32 list to binary for Redis
def float_to_bytes(vector):
    return b''.join([struct.pack('f', x) for x in vector])

# Root route to fix 404 error
@app.get("/")
def read_root():
    return {"message": "Welcome to the Neurofeed AI Semantic Search API!"}

# Optional: Check Redis connection on startup
@app.on_event("startup")
def check_redis():
    try:
        r.ping()
        print("✅ Redis is connected.")
    except redis.ConnectionError:
        print("❌ Redis connection failed.")

# Semantic vector search endpoint
@app.get("/search")
def search_articles(q: str = Query(..., description="Search query")):
    try:
        query_vector = model.encode(q)
        query_bytes = float_to_bytes(query_vector)

        redis_query = RedisQuery("*=>[KNN 3 @embedding $vec_param AS score]")\
            .return_fields("title", "content", "score")\
            .sort_by("score")\
            .dialect(2)

        params_dict = {
            "vec_param": query_bytes
        }

        results = r.ft("article_index").search(redis_query, query_params=params_dict)

        return [
            {
                "title": doc.title,
                "score": float(doc.score),
                "content": doc.content
            }
            for doc in results.docs
        ]

    except Exception as e:
        return {"error": str(e)}
