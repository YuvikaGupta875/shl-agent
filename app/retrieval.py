import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

print("Loading SHL catalog...")

with open("data/catalog.json", encoding="utf-8") as f:
    catalog = json.load(f)

print("Loading embedding model... (first run may take a minute)")

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []

for item in catalog:
    text = " ".join([
        item.get("name", ""),
        item.get("description", ""),
        " ".join(item.get("keys", [])),
        " ".join(item.get("job_levels", [])),
        " ".join(item.get("languages", []))
    ])
    documents.append(text)

print("Creating embeddings...")

doc_embeddings = model.encode(documents, show_progress_bar=True)


def search_catalog(query):
    query_embedding = model.encode([query])

    similarities = cosine_similarity(
        query_embedding,
        doc_embeddings
    )[0]

    top_indices = np.argsort(similarities)[::-1][:10]

    recommendations = []

    for idx in top_indices:
        item = catalog[idx]

        recommendations.append({
            "name": item["name"],
            "url": item["link"],
            "test_type": item["keys"][0] if item["keys"] else "Unknown"
        })

    return recommendations


def find_by_name(name):
    matches = []

    for item in catalog:
        if name.lower() in item["name"].lower():
            matches.append({
                "name": item["name"],
                "url": item["link"],
                "test_type": item["keys"][0] if item["keys"] else "Unknown",
                "description": item.get("description", "")
            })

    return matches