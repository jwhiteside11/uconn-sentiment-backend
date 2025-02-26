import subprocess
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import pandas as pd
import time
import os
from datastore_client import DatastoreClient, NewsDocument

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
  s_driver.get(f"https://www.google.com/search?q=yahoo+finance+{ticker}&tbs=cdr:1,cd_min:{start_date},cd_max:{end_date}&tbm=nws&num={num_articles}&rls=en")

  # select links of relevant text using <a> tag, filter yahoo news URLs
  links_elems = s_driver.wait_all_then_get(By.TAG_NAME, 'a')
  urls = [elem.get_attribute('href') for elem in links_elems]

  return [url for url in urls if url and 'finance.yahoo.com' in url]


'''
Scrape Yahoo Finance news story at specified URL for content of article

Output: dict representing news story info
Example usage:
  news_res = scrape_news_story("https://finance.yahoo.com/...")
'''
def scrape_news_story(url: str):
  source = fetch_utils.get_as_browser(url)
  if source.status_code != 200:
    print("Error:", source.status_code, source.text)
    return []

  # parse successful response
  html_content = source.text
  soup = BeautifulSoup(html_content, features="html.parser")

  # fetch relevant info: {title, date, text}
  title = soup.select_one(".cover-title").get_text()
  date = soup.select_one(".byline-attr-meta-time").get_text()
  article_body = soup.select_one(".body-wrap")
  paragraphs = article_body.find_all("p")

  return {
    "url": url, 
    "title": title, 
    "date": date, 
    "paragraphs": [p.get_text().replace('\xa0', ' ') for p in paragraphs]
  }


'''
Scrape 10 news stories from specified quarter for the specified ticker, save to GCP bucket

Example usage:
  save_news_stories("MSFT", 2024, 3)
'''
def save_news_stories(ticker: str, year: int, quarter: int):
  file_path = f'news-article-{ticker}-{year}Q{quarter}.xlsx'
  
  dfs = []
  urls = get_article_urls(ticker, year, quarter)

  for url in urls:
    res = scrape_news_story(url)
    if res:
      dfs.append(pd.DataFrame({res['date'] : [res['title'], res['url'], *(p for p in res['paragraphs'])]}))
    # sleep to avoid rate limiting
    time.sleep(2)

  df = pd.concat(dfs, axis=1, join='outer')
  # write dataframe to local file
  df.to_excel(file_path)

  # copy local file to google cloud
  subprocess.run(["gcloud", "storage", "cp", f"{file_path}", "gs://news-stories-raw/"])

  # remove local file
  os.remove(file_path)


def save_news_stories_to_datastore(ticker: str, year: int, quarter: int):
  ds = DatastoreClient()

  urls = get_article_urls(ticker, year, quarter)

  for url in urls:
    res = scrape_news_story(url)
    if res:
      news_doc = NewsDocument(ticker, **res)
      ds.createNewsStoryEntity(news_doc)
    # sleep to avoid rate limiting
    time.sleep(2)


# driver for running in production
def run_program():
  save_news_stories_to_datastore("WBS", 2024, 2)

# driver for testing different functions
def test_program():
  u = get_article_urls("MSFT", 2024, 3)
  print(u)


# main driver
if __name__ == "__main__":
  # test_program()
  run_program()