import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading SHL catalog...")

with open("data/catalog.json", encoding="utf-8") as f:
    catalog = json.load(f)

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

print("Building TF-IDF index...")

vectorizer = TfidfVectorizer(stop_words="english")

doc_vectors = vectorizer.fit_transform(documents)


def search_catalog(query, top_k=10):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, doc_vectors).flatten()

    top_indices = similarities.argsort()[::-1][:top_k]

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