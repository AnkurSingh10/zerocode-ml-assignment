from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os
import traceback 
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv() 

class RAGPipeline:
    def __init__(self):
        # Hugging Face API token and model
        self.api_token = os.getenv("HF_API_KEY")
        # self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        self.model_name = "HuggingFaceH4/zephyr-7b-beta"

        self.client = InferenceClient(model=self.model_name, token=self.api_token) 

        # Load FAISS index and QA data
        self.index = faiss.read_index(
            r"C:\Users\ankur\OneDrive\Desktop\learning\zc_assignment\Embeddings\faiss_index.index"
        )
        print("✅ FAISS index expects vector dimension:", self.index.d)

        with open(
            r"C:\Users\ankur\OneDrive\Desktop\learning\zc_assignment\Embeddings\qa_data.pkl", "rb"
        ) as f:
            data = pickle.load(f)
        self.questions = data["questions"]
        self.answers = data["answers"]
    
    def remote_embed(self, text):
        embed_url = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        
        import requests  
        response = requests.post(embed_url, headers=headers, json={"inputs": text})
        response.raise_for_status()
        output = response.json()
    
        if isinstance(output, list):
            if isinstance(output[0], list): 
                embedding = np.array(output[0])
            elif isinstance(output[0], float): 
                embedding = np.array(output)
            else:
                raise ValueError("Unexpected inner type in embedding response.")
        else:
            raise ValueError("Embedding format is not a list.")
        
        print(f"🔍 Final embedding shape: {embedding.shape}")
        return embedding.reshape(1, -1)

 
    def generate_answer(self, prompt):
        try:
            response = self.client.text_generation(
                prompt,
                max_new_tokens=256,
                temperature=0.4,
                return_full_text=False 
            )
            return response.strip()
        except Exception as e:
            print("❌ Error in generate_answer:", str(e))
            raise

    def answer_query(self, query, top_k=3):
        try:
            query_vec = self.remote_embed(query)
            query_vec = np.array(query_vec)
            query_vec = query_vec.reshape(1, -1)
    
            distances, indices = self.index.search(query_vec, top_k)
    
            
            retrieved_context = "\n".join(
                [f"Q: {self.questions[i]}\nA: {self.answers[i]}" for i in indices[0]]
            )
    
           
            prompt = f"""
You are a helpful medical assistant. Use the context below to answer the user’s question clearly and factually.

Context:
{retrieved_context}

Question: {query}
Answer:
"""


            print("🧾 Prompt being used:\n", prompt)
            return self.generate_answer(prompt).split("Answer:")[-1].strip()

        except Exception as e:
            print("❌ ERROR in answer_query:", str(e))
            traceback.print_exc()
            return "An internal error occurred."
