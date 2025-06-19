# client.py (interactive version)
import requests

while True:
    user_query = input("Ask a question (or type 'exit' to quit): ")
    if user_query.strip().lower() == "exit":
        break

    payload = {"query": user_query}
    try:
        response = requests.post("http://127.0.0.1:8000/chat", json=payload)

        if response.status_code == 200:
            print("🧠 Answer:", response.json()["response"], "\n")
        else:
            print("❌ Error:", response.status_code, response.text, "\n")
    except requests.exceptions.RequestException as e:
        print("🔌 Connection error:", e)
