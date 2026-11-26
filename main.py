from flask import Flask, request
import os
from dotenv import load_dotenv
from llm import chat_with_llm
from embedding import embed_text
from vector_store import search_chunks

from data.champions_league import RESULTS

load_dotenv()


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello Geeks"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("user_input")
    matches = search_chunks(user_input)
    context = "\n\n".join(m["text"] for m in matches)

    answer = chat_with_llm(user_input, context=context)
    return answer


@app.route("/embed", methods=["POST"])
def embed():

    embedding = embed_text(RESULTS)
    return embedding


@app.route("/search", methods=["POST"])
def search():
    data = request.json
    question = data.get("question")
    results = search_chunks(question)
    return results


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(debug=True, port=port)
