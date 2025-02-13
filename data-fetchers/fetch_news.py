import subprocess
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import pandas as pd
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import fetch_utils

# Selenium driver and util functions
s_driver = fetch_utils.SeleniumDriver()


'''
Scrape 10 URLs to Yahoo Finance news articles for a ticker in the date range specified

Output: list of URLs for scraping
Example usage:
  urls = get_article_urls("MSFT", year=2025, quarter=1)
'''
def get_article_urls(ticker: str, year: int, quarter: int) -> List[str]:
  [start_date, end_date] = fetch_utils.get_date_bounds(year, quarter)
  num_articles = 10
  # create Google search query for Yahoo Finance news about the ticker symbol
  source = fetch_utils.get_as_browser(f"https://www.google.com/search?q=yahoo+finance+{ticker}&tbs=cdr:1,cd_min:{start_date},cd_max:{end_date}&tbm=nws&num={num_articles}&rls=en")
  if source.status_code != 200:
    print("Error:", source.status_code, source.text)
    return
  
  # parse successful response
  html_content = source.text
  soup = BeautifulSoup(html_content, features="html.parser")

  # select links of relevant text using <a> tag, filter yahoo news URLs
  links_elems = soup.find_all('a')
  urls = [elem.attrs['href'] for elem in links_elems]

  results = []
  # hrefs in results are actually relative paths of format /url?p1=xxx&p2=...&url=<DATA_OF_INTEREST>&...
  # extract url of interest
  for url in urls:
    if 'finance.yahoo.com' not in url:
      continue
    start_ind = url.find("url=")
    results.append(url[start_ind + 4: url.find("&", start_ind)])

  return results


'''
Scrape Yahoo Finance news story at specified URL for content of article

Output: dict representing news story info
Example usage:
  news_res = news_stories("MSFT", year=2025, quarter=1)
'''
def scrape_news_story(url: str):
  # use selenium to simulate browser environment; screen dim 700x820
  s_driver.get(url)

  # see if paywall exists OR if we need to hit readmore button to access full article
  paywall_found = s_driver.wait_present(By.CLASS_NAME, "continue-reading", 10)
  if paywall_found:
    return None

  # if there is no paywall, check for readmore button; click if present
  try:
    s_driver.wait_then_click_elem(By.CLASS_NAME, "readmore-button", 1)
    time.sleep(1)
  except:
    pass

  # fetch relevant info: {title, date, text}
  title = s_driver.wait_present_then_do(By.CLASS_NAME, "cover-title", timeout=1).text
  date = s_driver.wait_present_then_do(By.CLASS_NAME, "byline-attr-meta-time", timeout=1).text
  article_body = s_driver.wait_present_then_do(By.CLASS_NAME, "body-wrap", lambda x: x, 1)
  paragraphs = article_body.find_elements(By.TAG_NAME, "p")

  return {
    "url": url, 
    "title": title, 
    "date": date, 
    "paragraphs": [p.text for p in paragraphs]
  }


'''
Scrape 10 news stories from specified quarter for the specified ticker, save to GCP bucket

Example usage:
  save_news_stories("MSFT", 2024, 3)
'''
def save_news_stories(ticker: str, year: int, quarter: int) -> Dict[Tuple[str, str], List[str]]:
  file_path = f'news-article-{ticker}-{year}Q{quarter}.xlsx'
  
  dfs = []
  urls = get_article_urls(ticker, year, quarter)

  for url in urls:
    try:
      res = scrape_news_story(url)
      dfs.append(pd.DataFrame({res['date'] : [res['title'], res['url'], *(p for p in res['paragraphs'])]}))
    except Exception as e:
      # catch WebDriverWait exceptions coming from selenium
      print(e)
      print('failed:', url)
    # sleep to avoid rate limiting
    time.sleep(2)

  df = pd.concat(dfs, axis=1, join='outer')
  # write dataframe to local file
  df.to_excel(file_path)

  # copy local file to google cloud
  subprocess.run(["gcloud", "storage", "cp", f"{file_path}", "gs://news-stories-raw/"])

  # remove local file
  os.remove(file_path)


# driver for running in production
def run_program():
  save_news_stories("MSFT", 2024, 4)

# driver for testing different functions
def test_program():
  u = get_article_urls("MSFT", 2024, 4)
  print(u)


# main driver
if __name__ == "__main__":
  test_program()
  # run_program()