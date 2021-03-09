from bs4 import BeautifulSoup as bs
import time, requests, logging, argparse, csv, os
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description="Popular Keyword Scraper")

parser.add_argument(
    "--begin", "-b", help="Enter date to start scraping from", type=str, required=True
)

parser.add_argument("--end", "-e", help="Enter the end date", type=str, required=True)

parser.add_argument(
    "--target", "-t", help="Enter the destination file", type=str, default="data.csv"
)

parser.add_argument(
    "--format", "-f", help="Enter the date format", type=str, default="%d/%m/%Y"
)

parser.add_argument(
    "--sleep", "-s", help="Enter the sleep duration (~2)", type=float, default=2
)

parser.add_argument(
    "--logging",
    "-l",
    help="Enter the name of logging file",
    type=str,
    default="logs.log",
)

args = parser.parse_args()

logging.basicConfig(
    filename=args.logging,
    filemode="w+",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}
BASE_URL = "https://getdaytrends.com/{}"


class Scraper:
    def __init__(
        self,
        HEADERS=HEADERS,
        BASE_URL=BASE_URL,
        sleep_step=args.sleep,
        target=args.target,
    ):
        self.HEADERS = HEADERS
        self.BASE_URL = BASE_URL
        self.sleep_step = sleep_step
        self.target = target
        self.writer = self.getWriter()

    def getWriter(self):
        fields = ["Hour", "Date", "Keyword", "Link", "TweetCount"]
        mode = "a"
        if not os.path.exists(self.target):
            mode = "a+"
        self.dat = open(self.target, mode, newline="")
        writer = csv.DictWriter(self.dat, fieldnames=fields)
        if mode == "a+":
            writer.writeheader()
        return writer

    def get_page(self, date, hour, country="india"):
        url = self.BASE_URL.format(f"{country}/{date}/{hour}")
        response = requests.get(url, headers=HEADERS)
        logging.debug("Page %s Scraped with %s" % (f"{date}/{hour}", str(response)))
        return bs(response.content, features="html.parser")

    def extract(self, page, day, hour):
        keywords = [tag.text for tag in page.table.findAll("a")]
        links = [tag.attrs["href"] for tag in page.table.findAll("a")]
        tweetcounts = [
            tag.text
            for tag in page.table.findAll("span", {"class": "small text-muted"})
        ]

        self.writer.writerows(
            [
                {
                    "Hour": hour,
                    "Keyword": keyword,
                    "Link": link,
                    "TweetCount": tweetcount,
                    "Date": day.strftime("%d-%m-%Y"),
                }
                for keyword, link, tweetcount in zip(keywords, links, tweetcounts)
            ]
        )

    def sleepstep(self):
        time.sleep(self.sleep_step)

    def scrape(self, begin, end, reg="%d/%m/%Y"):
        begin = datetime.strptime(begin, reg)
        assert begin.date() < datetime.now().date(), "Scraping a date from future"
        end = datetime.strptime(end, reg)
        current = begin
        step = timedelta(days=1)
        while current > end:
            current_date = current.strftime("%Y-%m-%d")
            for hour in range(24):
                page = self.get_page(current_date, str(hour))
                self.extract(page, current.date(), hour)
                self.sleepstep()
            current -= step


if __name__ == "__main__":
    scraper = Scraper(sleep_step=args.sleep)
    scraper.scrape(args.begin, args.end, args.format)
    scraper.dat.close()
