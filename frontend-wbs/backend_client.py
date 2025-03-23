import requests


class BackendClient:
  def __init__(self):
    self.DEV_URL: str = 'http://localhost:5100'
    self.PROD_VM_URL: str = 'http://34.44.103.189:5100'
    self.PUBLIC_API_URL: str = f'{self.PROD_VM_URL}/api'
    self.PUBLIC_AUTH_URL: str = f'{self.PROD_VM_URL}/auth'
    self.AUTH_PASSKEY = 'example'

  def GET(self, path: str):
    return requests.get(self.PUBLIC_API_URL + path)

  def search_news(self, ticker: str, search_term: str):
    return self.GET(f'/search_news?ticker={ticker}&search_term={search_term}')