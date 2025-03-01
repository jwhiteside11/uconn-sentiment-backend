import fetch_news
import fetch_utils
from datastore_client import DatastoreClient
from typesense_client import TypesenseClient, NewsDocument

class Fetcher:
  def __init__(self):
    self.ds = DatastoreClient()
    self.ts = TypesenseClient()

  def scrape_news(self, ticker: str):
    past_5_q = fetch_utils.get_past_8_quarters()[:5]
    results = []
    for (y, q) in past_5_q:
      res = fetch_news.scrape_news_stories_to_datastore(ticker, y, q)
      results += [{"message": f"error: {r["error"]}" if r["error"] else f"success: {r["url"]}"} for r in res]
    return results
  
  def scrape_earnings_calls(self, ticker: str):
    return None

  def get_news(self, ticker: str):
    return self.ds.getAllNewsDocs(ticker)

  def search_news(self, ticker: str, search_term: str):
    return self.ts.searchNews(ticker, search_term)

  def backfillTypesenseServer(self, ticker: str = ""):
    if ticker == "":
      print("resetting Typesense server")
      self.ts.deleteNewsColletion()
      self.ts.createNewsCollection()
    
    docs = self.ds.getAllNewsDocs(ticker)
    fails = 0
    for doc in docs:
      try:
        self.ts.createNewsDocument(doc)
        print("added: ", doc.id)
      except Exception as e:
        print("failed: ", doc.id)
        fails += 1

    return {"num_indexed": len(docs) - fails}
    
  def initTypesenseServer(self):
    try:
      self.ts.createNewsCollection()
    except:
      pass
    return {"message": "Typesense: news collection created"}