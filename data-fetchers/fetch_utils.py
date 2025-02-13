from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import datetime
from typing import List, Tuple


# use headers to mock authentic browser User-Agent in requests HTTP call
def get_as_browser(url):
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

def get_date_bounds(year: int, quarter: int) -> Tuple[str, str]:
  starts = ["01/01", "04/01", "07/01", "10/01"]
  ends   = ["03/31", "06/30", "09/30", "12/31"]
  start_date, end_date = f"{starts[quarter-1]}/{year}", f"{ends[quarter-1]}/{year}"
  return [start_date, end_date]


class SeleniumDriver:
    # Configure Selenium webdriver using chromedriver - requires Chrome installation
    # ------------------------------------------------
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=700x820")

        self.driver = webdriver.Chrome(options=chrome_options)

    # Functions used to wait for elements to appear on webpage
    # Without waits, program has lots of errors trying to process page elements that haven't loaded
    # ------------------------------------------------
    def wait_then_do(self, by, locator, ec, func = lambda x: x, timeout = 10):
        element = WebDriverWait(self.driver, timeout).until(ec((by, locator)))
        return func(element)
            
    def wait_all_then_get(self, by, locator, timeout = 10):
        return self.wait_then_do(by, locator, EC.presence_of_all_elements_located, lambda x: x, timeout)

    def wait_present_then_do(self, by, locator, func = lambda x: x, timeout = 10):
        return self.wait_then_do(by, locator, EC.presence_of_element_located, func, timeout)
        
    def wait_clickable_then_do(self, by, locator, func = lambda x: x, timeout = 10):
        return self.wait_then_do(by, locator, EC.element_to_be_clickable, func, timeout)
        
    def wait_then_click_elem(self, by, locator, timeout = 10):
        return self.wait_clickable_then_do(by, locator, lambda elem: elem.click(), timeout)
        
    def wait_then_send_keys(self, by, locator, keys, timeout = 10):
        return self.wait_clickable_then_do(by, locator, lambda elem: elem.send_keys(keys), timeout)
    
    def wait_present(self, by, locator, timeout = 10):
        try:
          self.wait_then_do(by, locator, EC.presence_of_element_located, timeout=timeout)
        except:
           return False
        return True
    
    def get(self, url):
       return self.driver.get(url)