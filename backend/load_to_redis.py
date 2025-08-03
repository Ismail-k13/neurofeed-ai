# load_to_redis.py

import json
import redis
import os
import struct
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

# Redis connection
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=False
)

INDEX_NAME = "articles-idx"
VECTOR_DIM = 384  # for all-MiniLM-L6-v2
VECTOR_TYPE = "FLAT"
DISTANCE_METRIC = "COSINE"
DOC_PREFIX = "doc:"

# Delete old index if exists
try:
    r.ft(INDEX_NAME).dropindex(delete_documents=False)
except Exception:
    pass

# Create index
r.ft(INDEX_NAME).create_index(
    fields=[
        TextField("title"),
        TextField("content"),
        VectorField(
            "embedding",
            VECTOR_TYPE,
            {
                "TYPE": "FLOAT32",
                "DIM": VECTOR_DIM,
                "DISTANCE_METRIC": DISTANCE_METRIC,
                "INITIAL_CAP": 1000,
            },
        ),
    ],
    definition=IndexDefinition(prefix=[DOC_PREFIX], index_type=IndexType.HASH)
)

# Load embeddings
with open("data/embedded_articles.json", "r") as f:
    articles = json.load(f)

# Insert into Redis
for article in articles:
    key = f"{DOC_PREFIX}{article['id']}"
    r.hset(
        key,
        mapping={
            "title": article["title"],
            "content": article["content"],
            "embedding": struct.pack(f"{VECTOR_DIM}f", *article["embedding"]),
        }
    )

print("✅ Successfully uploaded articles into Redis")
