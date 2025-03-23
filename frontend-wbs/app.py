from backend_client import BackendClient
from flask import Flask, jsonify, render_template, request
import json

api_client = BackendClient()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("hello.html")


# Search news using Typesense
@app.route('/search_news', methods=['GET'])
def search_news():
    return render_template("search_news.html")


if __name__ == "__main__":
    app.run(debug=True)