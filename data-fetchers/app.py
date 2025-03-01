from fetcher import Fetcher
from flask import Flask, jsonify, request

fetcher = Fetcher()
fetcher.initTypesenseServer()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")


# Backfill Typesense server with Datastore content
@app.route('/backfill_typesense', methods=['GET'])
def backfill():
    ticker = request.args.get("ticker")
    res = fetcher.backfillTypesenseServer(ticker)
    return jsonify(res)


# Search news using Typesense
@app.route('/search_news', methods=['GET'])
def search_news():
    ticker = request.args.get("ticker")
    search_term = request.args.get("search_term")
    res = fetcher.search_news(ticker, search_term)
    return jsonify(res)


# Scrape news using Selenium and requests, stores in Datastore
@app.route('/scrape_news', methods=['GET'])
def scrape_news():
    ticker = request.args.get("ticker")
    res = fetcher.scrape_news(ticker)
    return jsonify({"num_attempts": len(res), "num_success": len([r for r in res if not r["error"]]), "results": res})




if __name__ == "__main__":
    app.run(debug=True)