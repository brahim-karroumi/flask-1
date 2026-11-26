from flask import Flask , request
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)


@app.route("/")
def home():
    return "Hello Geeks"

@app.route("/chat" , methods=["POST"])
def chat():
    data = request.json()
    message = data.get("message")
    return message


if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(debug=True, port=port)
