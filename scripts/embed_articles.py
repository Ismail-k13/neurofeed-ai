import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Load news articles
with open("../data/articles.json", "r") as f:
    articles = json.load(f)

# Load HuggingFace embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create a new list with vector embeddings
embedded_articles = []

for article in tqdm(articles):
    text = f"{article['title']} {article['content']}"
    embedding = model.encode(text).tolist()
    embedded_articles.append({
        "id": article["id"],
        "title": article["title"],
        "content": article["content"],
        "embedding": embedding
    })

# Save as embedded_articles.json
with open("../data/embedded_articles.json", "w") as f:
    json.dump(embedded_articles, f, indent=2)

print("✅ Embeddings saved to embedded_articles.json")
