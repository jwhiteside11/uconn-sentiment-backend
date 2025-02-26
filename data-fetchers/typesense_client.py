import typesense
import json
import sys

class NewsDocument:
    def __init__(self, ticker, date, title, url, paragraphs):
        self.ticker = ticker
        self.date = date
        self.title = title
        self.url = url
        self.paragraphs = paragraphs


class TypesenseClient:
    def __init__(self):
        self.client = typesense.Client({
            'api_key': 'Hu52dwsas2AdxdE',
            'nodes': [{
                'host': 'localhost',
                'port': '8108',
                'protocol': 'http'
            }],
            'connection_timeout_seconds': 2
        })

    def createNewsCollection(self):
        return self.client.collections.create({
            "name": "news",
            "fields": [
                {"name": "ticker", "type": "string" },
                {"name": "date", "type": "string" },
                {"name": "title", "type": "string" },
                {"name": "url", "type": "string" },
                {"name": "paragraphs", "type": "string[]" },
            ]
        })

    def createNewsDocument(self, news_doc: NewsDocument):
        self.client.collections['news'].documents.create(news_doc.__dict__)

    def searchNews(self, ticker, search_term):
        search_parameters = {
            'q'         : search_term,
            'query_by'  : 'paragraphs',
            'filter_by' : f'ticker:={ticker}'
        }

        res = self.client.collections['news'].documents.search(search_parameters)
        return json.dumps(res, indent=4)

    def deleteNewsColletion(self):
        self.client.collections['news'].delete()
        
def run_program(ticker, search_term):
    # Create client
    ts = TypesenseClient()

    # Search documents
    res = ts.searchNews(ticker, search_term)
    print(res)

def test_program():
    # 1) Create client
    ts = TypesenseClient()

    # 2) Create collection
    ts.createNewsCollection()

    # 3) Add some documents
    doc1 = NewsDocument("WBS", "August 20, 2024", "Microsoft's dominant 21st century offers a key lesson for stock market investors: Morning Brief", "https://finance.yahoo.com/news/microsofts-dominant-21st-century-offers-a-key-lesson-for-stock-market-investors-morning-brief-100009433.html", 
                        [
                            "This is The Takeaway from today's Morning Brief, which you can sign up to receive in your inbox every morning along with:",
                            "The chart of the day",
                            "What we're watching",
                            "What we're reading",
                            "Economic data releases and earnings",
                            "When the economic cycle actually turns, the biggest drivers of the stock market will change.",
                            "An obvious statement, perhaps. But the current market rebound is being led by the same handful of Big Tech winners that have dominated both returns and the market conversation since 2023.",
                            "And until these terms and conditions change, this remains the AI moment.",
                            "In a note to clients on Monday, strategists at Bank of America led by Michael Hartnett looked at the 10 largest companies in the world at four distinct points this century — March 2000, November 2007, March 2009, and November 2021 — plus the end of July of this year.",
                            "These dates represent, respectively: the top of the market before the tech bust, the top before the financial crisis, the bottom of the financial crisis, and the market's highs reached after the pandemic. And today, global stocks are trading at basically record levels.",
                            "In this exercise, BofA teases out two key features of any market always worth keeping in mind for investors — composition and concentration.",
                            "On the first, investors need to remember that the names we view as market leaders are always changing. And when the cycle really does change, so too will the market's leaders.",
                            "Microsoft (MSFT), for instance, is the only company to rank among the world's largest 10 companies at each of these checkpoints over the last nearly 25 years. In fact, Microsoft is the only company currently in the top 10 to rank on any of the three dates before 2021.",
                            "In reading this note, we were reminded of the exercise Warren Buffett did at the top of Berkshire Hathaway's annual meeting back in 2021, when he looked at how the world's 20 biggest companies had changed over the prior 30 years.",
                            "\"It is a reminder of what extraordinary things can happen,\" Buffett said back in 2021. \"The world can change, and [in] very, very dramatic ways.\"",
                            "Since 2009, there's been 90% turnover among the world's 10 biggest companies. Fifteen years ago, there were four companies from China in the top 10. Today, there are none.",
                            "Apple (AAPL), currently the world's largest company, didn't appear on BofA's rankings until its 2021 edition. (In 2014, Apple was the world's largest company; by 2018, it had become the first US company to see its market value cross $1 trillion.)",
                            "Of course, had BofA chosen to select an intermediate date between 2009 and 2021 — say, the stock market's high in the summer of 2015 that wouldn't be overtaken for a year — the list wouldn't be quite as dramatically different: Apple, Microsoft, and Alphabet (GOOG, GOOGL) would all feature in the rankings. But still, those would be the only three holdovers from nine years ago.",
                            "Concentration in the stock market has also changed dramatically over time. In 2009, the top 10 companies in the world accounted for about 10% of global market cap; today, that ratio is closer to 25%.",
                            "Looking at 2000, 2007, and 2021, however, we see concentration looks more similar — though still less extreme — than today. The world's 10 biggest companies accounted for 17%, 11.6%, and 21.2% of global market in each of those years, respectively.",
                            "So not only has the market become significantly more tech-forward and US-centric, but also more concentrated.",
                            "Whether an investor sees these past and present states of play as good, bad, or indifferent is what makes a market. The numbers simply tell us what is.",
                            "But that only Microsoft has maintained its place among the global elite over the last quarter century tells us what is most likely to happen over the next 25 years.",
                            "Click here for the latest stock market news and in-depth analysis, including events that move stocks",
                            "Read the latest financial and business news from Yahoo Finance",
                        ])

    ts.createNewsDocument(doc1)

    # 4) Search documents
    res = ts.searchNews("WBS", "AI")
    print(res)



if __name__ == "__main__":
    ticker = sys.argv[1]
    search_term = sys.argv[2]

    run_program(ticker, search_term)