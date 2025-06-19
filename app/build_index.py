from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np
import pickle

# Load dataset
df = pd.read_csv("Embeddings\QA.csv")

# 🔥 Limit to a smaller subset (adjust as needed)
MAX_ENTRIES = 1000 #>=400
df = df.head(MAX_ENTRIES)

# Extract questions and answers
questions = df["question"].tolist()
answers = df["answer"].tolist()

# Embed using SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(questions)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Save index and data
faiss.write_index(index, "Embeddings\faiss_index.index")
with open("Embeddings\qa_data.pkl", "wb") as f:
    pickle.dump({"questions": questions, "answers": answers}, f)

print("index and QA data saved.")
