# Data fetching service for the Sentiment project

This subfolder holds all of the code to:
1. Scrape financial news from Yahoo finance and store in Datastore.
2. Get news stories directly from Datastore.
3. Search news data using Typesense.

The code is designed to run on the Compute Engine VM. This subfolder uses Docker to containerize different parts of the application. We will have one container for the Typesense server, and one for the Python code herein.

# Quick start

First, SSH into the VM.

From there, pull the code into the VM.
```bash
# if you don't already have the code base on your VM
git clone https://github.com/jwhiteside11/uconn-sentiment-backend.git

# if you DO already have the code, the following will update
git pull https://github.com/jwhiteside11/uconn-sentiment-backend.git
```

Navigate to this subfolder.
```bash
cd uconn-sentiment-backend/data-fetchers
```

From here, we must get Docker up and running. Begin by installing Docker on your VM instance.
```bash
sudo apt install docker.io
```

To run these containers on our VM at the same time, we will use the shell command `tmux`. If you are not already familiar, review [this guide](https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) before proceeding.

Then, we must pull the Typesense image, and run it on our VM. 
```bash
tmux new-session -A -t typesense

# from tmux session
sudo docker pull typesense/typesense:28.0

sudo docker run -p 8108:8108 -v/tmp/data:/data typesense/typesense:28.0 --data-dir /data --api-key=Hu52dwsas2AdxdE
# (Ctrl + B) + D
```

Now, Typesense is up and running in a container, and accessible via HTTP. 

We are going to do pretty much the same for the Python code we wrote, this time using a local Dockerfile.
```bash
tmux new-session -A -t fetch_server

# from tmux session
sudo docker build --tag fetch_server .

sudo docker run --add-host=host.docker.internal:host-gateway -p 5000:5000 fetch_server
# (Ctrl + B) + D
```

So we have two Docker containers up and running. To interact with these services, we can use HTTP calls.

Everything is now up and running. Test the server using the `Hello world!` example.
```bash
curl 'localhost:5000/'
```

**Note:** each time the Typesense server is restarted, it must be backfilled with the news we've scraped into datastore. There is an endpoint for doing so.
```bash
curl 'localhost:5000/backfill_typesense'
```

&nbsp;

# API reference
This code is wrapped with a Flask server. Interact with this code base using HTTP calls to `localhost:5000`. 

In the examples above, I use the `curl` shell command, but you can interface with the containers any HTTP library in any language.

## Endpoints

### GET /scrape_news

Scrape news from Yahoo Finance using Selenium and requests.

#### Request
- **Method**: GET
- **URL**: `/scrape_news`

#### Query Parameters
| Parameter    | Type   | Description                        |
|--------------|--------|------------------------------------|
| `ticker`       | str    | The ticker of the company of interest (required). |

#### Example Request
`curl localhost:5000/scrape_news?ticker=WBS`

#### Response
- **Status Code**: 200 OK
- **Content-Type**: `application/json`

```json
{
  "num_attempts": 4, 
  "num_success": 3, 
  "results": [
    {"message": "success: https://finance.yahoo.com/news/curious-webster-financial-wbs-q4-141510242.html"},
    {"message": "failed: already scraped url https://finance.yahoo.com/news/webster-financial-corporation-wbs-best-093505383.html"},
    {"message": "success: https://finance.yahoo.com/news/webster-financials-nyse-wbs-dividend-120809687.html"},
    {"message": "success: https://finance.yahoo.com/news/earnings-preview-webster-financial-wbs-150010712.html"},
  ]
}
```
---

### GET /search_news

Search for news using Typesense server.

#### Request
- **Method**: GET
- **URL**: `/search_news`

#### Query Parameters
| Parameter    | Type   | Description                        |
|--------------|--------|------------------------------------|
| `ticker`       | str    | The ticker of the company of interest (required). |
| `search_term`  | str    | The word/phrase to search for (required). |

#### Example Response
- **Status Code**: 200 OK
- **Content-Type**: `application/json`

```json
{
  "num_hits": 1, 
  "hits": [
    {
      "title": "Curious about Webster Financial (WBS) Q4 Performance? Explore Wall Street Estimates for Key Metrics",
      "url": "https://finance.yahoo.com/news/curious-webster-financial-wbs-q4-141510242.html", 
      "highlights": [
        ...
      ]
    }
  ]
}
```
---

### GET /backfill_typesense

Backfill Typesense server with news articles from Datastore.

#### Request
- **Method**: GET
- **URL**: `/backfill_typesense`

#### Query Parameters
| Parameter    | Type   | Description                        |
|--------------|--------|------------------------------------|
| `ticker`       | str    | The ticker of the company of interest (optional; if not provided, evrey news document in the Datastore will be indexed). |

#### Example Response
- **Status Code**: 200 OK
- **Content-Type**: `application/json`

```json
{
  "num_indexed": 16
}
```