import subprocess
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import pandas as pd
import datetime
import time
import os


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
def earnings_calls(ticker: str, year: int, quarter: int) -> List[str]:
  source = get_as_browser(f"https://www.roic.ai/quote/{ticker}/transcripts/{year}-year/{quarter}-quarter")
  if source.status_code != 200:
    print("ERROR:", source)
    return
  
  # parse successful response
  html_content = source.text
  soup = BeautifulSoup(html_content, features="html.parser")
  # select paragraphs of relevant text using CSS selector
  paragraphs = soup.select('p.pb-4')
  return [p.get_text() for p in paragraphs]


'''
Scrape earning calls for the past 8 quarters for the specified ticker

Output: dict object mapping (year, quarter) keyed lists of paragraphs
Example usage:
  earnings_dict = save_earnings_calls("MSFT")
'''
def save_earnings_calls(ticker: str) -> Dict[Tuple[str, str], List[str]]:
  past8q = get_past_8_quarters()
  
  [[firsty, firstq], [lasty, lastq]] = [past8q[-1], past8q[0]]
  file_path = f'earnings-call-{ticker}-{firsty}Q{firstq}-{lasty}Q{lastq}.xlsx'

  dfs = []
  i = 0
  for (year, quarter) in past8q:
    res = earnings_calls(ticker, year, quarter)
    dfs.append(pd.DataFrame({f"{year} Q{quarter}" : res}))
    # sleep to avoid rate limiting
    time.sleep(2)

  df = pd.concat(dfs, axis=1, join='outer')
  # write dataframe to local file
  df.to_excel(file_path)

  # copy local file to google cloud
  subprocess.run(["gcloud", "storage", "cp", f"{file_path}", "gs://earnings-calls-raw/"])

  # remove local file
  os.remove(file_path)



# driver for running in production
def run_program():
  save_earnings_calls("MSFT")

# driver for testing different functions
def test_program():
  q = get_past_8_quarters()
  print(q)


# main driver
if __name__ == "__main__":
  test_program()
  # run_program()