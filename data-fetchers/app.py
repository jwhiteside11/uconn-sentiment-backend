from fetcher import Fetcher
from flask import Flask, jsonify, request
from flask_cors import CORS

fetcher = Fetcher()
fetcher.initTypesenseServer()

app = Flask(__name__)

CORS(app, supports_credentials=True, origins=['http://sentiment-test-417820.uc.r.appspot.com'])

@app.before_request
def before_request():
    token = request.headers.get("WBS-API-PASSKEY")
    print("GET THE TOKEN", token)
    if not token:
        token = request.cookies.get("WBS-API-PASSKEY")
        if not token:
            return jsonify({"message": "Passkey is missing."}), 403

    tokenRes = fetcher.auth.validate_passkey(token)
    print(tokenRes)
    if "valid" not in tokenRes or not tokenRes["valid"]:
        return jsonify({"message": tokenRes["error"]}), 403


@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")


# Scrape news using Selenium and requests, stores in Datastore
@app.route('/scrape_news', methods=['GET'])
def scrape_news():
    ticker = request.args.get("ticker", default="")
    if ticker == "":
        return jsonify({"message": "missing required query param: ticker"}), 400
    
    res = fetcher.scrape_news(ticker)
    return jsonify({"num_attempts": len(res), "num_success": len([r for r in res if "error" not in r]), "results": res})


@app.route('/search_news', methods=['GET'])
def search_news():
    ticker = request.args.get("ticker", default="")
    if ticker == "":
        return jsonify({"message": "missing required query param: ticker"}), 400
    
    search_term = request.args.get("search_term", default="")

    res = fetcher.search_news(ticker, search_term)
    return jsonify(res)


# Get tickers indexed in typesense
@app.route('/search_news/indexed_tickers', methods=['GET'])
def indexed_tickers():
    res = fetcher.ts.getIndexedTickers()
    return jsonify(res)


# Get tickers indexed in typesense
@app.route('/search_news/summary', methods=['GET'])
def summarize():
    ticker = request.args.get("ticker", default="")
    if ticker == "":
        return jsonify({"message": "missing required query param: ticker"}), 400
    
    res = fetcher.get_summary(ticker)
    return jsonify(res)


@app.route('/score_news', methods=['GET'])
def score_news():
    ticker = request.args.get("ticker", default="")
    if ticker == "":
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