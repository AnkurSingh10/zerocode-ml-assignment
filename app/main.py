#main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from rag import RAGPipeline

app = FastAPI()
rag_pipeline = RAGPipeline()

class Query(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: Query):
    try:
        question = request.query
        answer = rag_pipeline.answer_query(question)

        # ANSI escape code for bold: \033[1m...\033[0m
        formatted_response = (
            f"\033[1mQuestion:\033[0m {question}\n\n"
            f"\033[1mAnswer:\033[0m\n\n"
            f"\033[1m{answer}\033[0m"
        )

        return {"response": formatted_response}
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"response": "An internal error occurred."}
