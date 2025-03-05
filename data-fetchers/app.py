from fetcher import Fetcher
from flask import Flask, jsonify, request

fetcher = Fetcher()
fetcher.initTypesenseServer()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")


# Scrape news using Selenium and requests, stores in Datastore
@app.route('/scrape_news', methods=['GET'])
def scrape_news():
    ticker = request.args.get("ticker")
    if ticker is None:
        return jsonify({"message": "missing required query param: ticker"}), 400
    
    res = fetcher.scrape_news(ticker)
    return jsonify({"num_attempts": len(res), "num_success": len([r for r in res if "error" not in r]), "results": res})


# Search news using Typesense
@app.route('/search_news', methods=['GET'])
def search_news():
    ticker = request.args.get("ticker")
    if ticker is None:
        return jsonify({"message": "missing required query param: ticker"}), 400
    
    search_term = request.args.get("search_term")

    res = fetcher.search_news(ticker, search_term)
    return jsonify(res)


@app.route('/score_news', methods=['GET'])
def score_news():
    ticker = request.args.get("ticker")
    if ticker is None:
        return jsonify({"message": "missing required query param: ticker"}), 400
    
    res = fetcher.score_news(ticker)
    return jsonify({"num_attempts": len(res), "num_success": len([r for r in res if "error" not in r]), "results": res})


# Backfill Typesense server with Datastore content
@app.route('/backfill_typesense', methods=['GET'])
def backfill():
    ticker = request.args.get("ticker")
    
    res = fetcher.backfillTypesenseServer(ticker)
    return jsonify(res)




if __name__ == "__main__":
    app.run(debug=True)