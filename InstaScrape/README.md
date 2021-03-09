# InstaScrape
This is a scraper for scraping top search results on Instagram

## Requirements
* python3
* selenium
* pandas

## Usage
```python
from scraper import InstaScraper

#Bot init
scrape_bot = InstaScraper()

#OAuth Authentication
scrape_bot.login('<YOUR USERNAME>', '<YOUR PASSWORD>')

#Get URL
scrape_bot.get_loc("Enter Search Item Here")
```

## Running
```shell
git clone https://github.com/someshsingh22/InstaScrape
cd InstaScrape
python3 script.py
```