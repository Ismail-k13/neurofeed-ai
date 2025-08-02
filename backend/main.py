import struct
import json
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.index_definition import IndexDefinition

# Helper: convert float list to binary
def float_to_bytes(vector):
    return b"".join([struct.pack("f", x) for x in vector])

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=False)

INDEX_NAME = "article_index"
VECTOR_DIM = 384

# Drop existing index if it exists
try:
    r.ft(INDEX_NAME).dropindex(delete_documents=True)
except:
    pass

# Define schema
schema = (
    TextField("title"),
    TextField("content"),
    VectorField("embedding", "FLAT", {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DIM,
        "DISTANCE_METRIC": "COSINE"
    })
)

# Create the index
r.ft(INDEX_NAME).create_index(schema, definition=IndexDefinition(prefix=["article:"]))

# Load articles from JSON
with open("../data/embedded_articles.json", "r") as f:
    articles = json.load(f)

# Store to Redis
pipe = r.pipeline()
for article in articles:
    key = f"article:{article['id']}"
    pipe.hset(key, mapping={
        "title": article["title"],
        "content": article["content"],
        "embedding": memoryview(float_to_bytes(article["embedding"]))
    })

pipe.execute()

print("✅ All vectors loaded into Redis")
