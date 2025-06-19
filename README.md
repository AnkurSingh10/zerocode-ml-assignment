# zerocode-ml-assignment

## 🔧 Features
- RAG with HuggingFaceH4/zephyr-7b-beta
- FAISS for semantic retrieval
- FastAPI server `/chat`
- Evaluation pipeline for comparison
- Dockerized

## 🚀 Run
```bash
python app/build_index.py
uvicorn app.main:app --reload
python evaluation/eval.py
```

## 🐳 Docker
```bash
docker-compose up --build
```

## 🧪 Test
```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query": "What is Glaucoma?"}'
