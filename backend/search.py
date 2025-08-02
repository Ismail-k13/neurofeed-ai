import redis
import struct
from sentence_transformers import SentenceTransformer
from redis.commands.search.query import Query  # ✅ Correct import

def float_to_bytes(vector):
    return b"".join([struct.pack("f", x) for x in vector])

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=False)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Query sentence
query_text = "What is Meta's latest open-source AI model?"

# Generate embedding
query_vector = model.encode(query_text)
query_bytes = float_to_bytes(query_vector)

# Build query using vector similarity
q = f'*=>[KNN 3 @embedding $vec_param AS score]'
params_dict = {
    "vec_param": query_bytes
}

# ✅ Correct way to define query
query = Query(q).return_fields("title", "content", "score").sort_by("score").dialect(2)

# Search
results = r.ft("article_index").search(query, query_params=params_dict)

# Display
for doc in results.docs:
    print(f"Title: {doc.title}")
    print(f"Score: {doc.score}")
    print(f"Content: {doc.content}\n")
