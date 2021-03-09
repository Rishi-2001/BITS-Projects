# Hindi NLP
* Folder [Link](https://drive.google.com/drive/folders/19dSsQxsVqpdrIEqbL5VZByC814exzXi6?usp=sharing)

## KeyWord Scraper

### Dependency
* Python3
* BeautifulSoup4

### Usage

#### CLI
```bash
#Returns you all available options
>>> python3 -h keywordscrape.py
  -h, --help            show this help message and exit
  --begin BEGIN, -b BEGIN
                        Enter date to start scraping from
  --end END, -e END     Enter the end date
  --target TARGET, -t TARGET
                        Enter the destination file
  --format FORMAT, -f FORMAT
                        Enter the date format
  --sleep SLEEP, -s SLEEP
                        Enter the sleep duration (~2)
  --logging LOGGING, -l LOGGING
                        Enter the name of logging file
```

#### Python
```python
from keywordscrape import * #Imports

scraper = Scraper(sleep_step=2) #Set Default sleep for preventing DNS Blocking

#Enter Start date, End date and date format
data = scraper.scrape("01/09/2020", "24/08/2020", format="%d/%m/%Y") 

#Save as JSON
with open("data.json", "w+") as fp:
    json.dump(data, fp)
```
