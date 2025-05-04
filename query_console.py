# Author: ChatGPT
# scripts/query_console.py

from app.indexing.index import load_index
from app.indexing.id_map import load_id_map
from app.retrieval.retriever import query_llm
from app.ingestion.storage import conn
from app.config import MODEL_NAME
from sentence_transformers import SentenceTransformer
import numpy as np

# Load SentenceTransformer model and FAISS index
model = SentenceTransformer(MODEL_NAME)
index = load_index(384)  # Embedding size for MiniLM
id_map = load_id_map()

# Function to handle user query
def query_data(query):
    # Convert query to embedding
    query_vector = np.array([model.encode(query)], dtype="float32")

    # Perform nearest neighbor search on FAISS index
    D, I = index.search(query_vector, 3)

    results = []
    for idx in I[0]:
        if idx < len(id_map):
            file_hash = id_map[idx]
            cur = conn.execute("SELECT text FROM images WHERE id=?", (file_hash,))
            row = cur.fetchone()
            if row:
                results.append(row[0])

    if results:
        context = "\n---\n".join(results)
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        answer = query_llm(prompt)
        return answer
    else:
        return "No matching documents found."

# Main loop for querying the system
def main():
    print("Welcome to the Screenshot Chatbot!")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        query = input("Ask me: ")
        if query.lower() in ["exit", "quit"]:
            break

        answer = query_data(query)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
