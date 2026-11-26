from flask import Flask, request
import os
from dotenv import load_dotenv
from llm import chat_with_llm

load_dotenv()


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello Geeks"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("user_input")
    

    answer = chat_with_llm(user_input)
    return answer


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(debug=True, port=port)
