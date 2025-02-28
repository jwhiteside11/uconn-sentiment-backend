import fetch_news
from datastore_client import DatastoreClient
from typesense_client import TypesenseClient, NewsDocument

class Fetcher:
  def __init__(self):
    self.ds = DatastoreClient()
    self.ts = TypesenseClient()

  def scrape_news(self, ticker: str):
    return fetch_news.save_news_stories_to_datastore(ticker, 2024, 4)
  
  def scrape_earnings_calls(self, ticker: str):
    return None

  def get_news(self, ticker: str):
    return self.ds.getAllNewsDocs(ticker)

  def search_news(self, ticker: str, search_term: str):
    return self.ts.searchNews(ticker, search_term)

  def backfillTypesenseServer(self, ticker: str = ""):
    self.ts.deleteNewsColletion()
    self.ts.createNewsCollection()

    docs = self.ds.getAllNewsDocs(ticker)
    for doc in docs:
      try:
        self.ts.createNewsDocument(doc)
        print("added: ", doc.id)
      except Exception as e:
        print("failed: ", doc.id)
    
  def initTypesenseServer(self):
    try:
      self.ts.createNewsCollection()
    except:
      pass