# Author: ChatGPT
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import MODEL_NAME
from app.indexing.id_map import load_id_map
from app.indexing.index import load_index
from app.ingestion.storage import conn
from app.retrieval.retriever import query_llm

model = SentenceTransformer(MODEL_NAME)
index = load_index(384)
id_map = load_id_map()

while True:
    query = input("Ask me: ")
    if query.lower() in ["exit", "quit"]:
        break

    q_vec = np.array([model.encode(query)], dtype="float32")
    D, I = index.search(q_vec, 3)

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
        print(f"Answer: {answer}")
    else:
        print("No matching documents found.")
