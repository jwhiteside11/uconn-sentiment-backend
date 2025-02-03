import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import datetime


def get_as_browser(url):
  # use headers to mock authentic browser User-Agent in requests HTTP call
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  return requests.get(url, headers=headers)

def get_current_quarter() -> Tuple[int, int]:
  date_object = datetime.datetime.now()

  month = date_object.month
  year = date_object.year
  qtr = (month - 1) // 3 + 1
  return (year, qtr)


def get_past_8_quarters() -> List[Tuple[int, int]]:
  [currY, currQ] = get_current_quarter()
  res = [(currY, currQ)]
  while len(res) < 8:
    currQ -= 1
    if currQ == 0:
      currY -= 1
      currQ = 4
    res.append((currY, currQ))
  return res



'''
Scrape a specified earning calls from roic

Output: paragraphs from the specified earnings call
Example usage:
  p_res = earnings("MSFT", year=2025, quarter=1)
'''
def earnings(ticker: str, year: int, quarter: int) -> List[str]:
  source = get_as_browser(f"https://www.roic.ai/quote/{ticker}/transcripts/{year}-year/{quarter}-quarter")
  if source.status_code != 200:
    print("ERROR:", source)
    return
  
  # parse successful response
  html_content = source.text
  soup = BeautifulSoup(html_content, features="html.parser")
  # select paragraphs of relevant text using CSS selector
  paragraphs = soup.select('p.pb-4')
  return paragraphs


'''
Scrape earning calls for the past 8 quarters for the specified tickers

Output: dict object mapping tickers to a dict of (year, quarter) keyed lists of paragraphs
Example usage:
  earnings_dict = scrape_earnings(["MSFT", "APPL", "YHOO"])
'''
def scrape_earnings(tickers: List[str]) -> Dict[str, Dict[Tuple[str, str], List[str]]]:
  past8q = get_past_8_quarters()
  
  res = {}
  for ticker in tickers:
    res[ticker] = {}
    for (year, quarter) in past8q:
      res[ticker][(year, quarter)] = earnings(ticker, year, quarter)
  
  return res



# driver for running in production
def run_program():
  pass

# driver for testing different functions
def test_program():
  q = get_past_8_quarters()
  print(q)


# main driver
if __name__ == "__main__":
  test_program()
  # run_program()