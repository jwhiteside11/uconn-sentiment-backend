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
    res = api_client.get_tickers().json()
    return render_template("search_news.html", ticker_list=res["tickers"])


# Data visualization graphs
@app.route('/graph_news', methods=['GET'])
def graph():
    ticker_res = api_client.get_tickers().json()
    summary_res = api_client.get_summary("WBS").json()
    return render_template("graphs_example.html", ticker_list=ticker_res["tickers"], summary=summary_res)


if __name__ == "__main__":
    app.run(debug=True)