from fetcher import Fetcher
from flask import Flask, jsonify, request

fetcher = Fetcher()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

# Search news using Typesense
@app.route('/search', methods=['GET'])
def search():
    ticker = request.args.get("ticker")
    search_term = request.args.get("search_term")
    res = fetcher.search_news(ticker, search_term)
    return jsonify(res)

# Scrape news using Selenium and requests, stores in Datastore
@app.route('/scrape_news', methods=['GET'])
def scrape_news():
    ticker = request.args.get("ticker")
    res = fetcher.scrape_news(ticker)
    return jsonify(res)

# Get news document from Datastore
@app.route('/news', methods=['GET'])
def get_news():
    ticker = request.args.get("ticker")
    res = fetcher.scrape_news(ticker)
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)