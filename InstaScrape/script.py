from scraper import InstaScraper
import pandas as pd
import time

# Change required Path here
CSV_PATH = "./insta.csv"

# Bot init
scrape_bot = InstaScraper()

# OAuth Authentication
scrape_bot.login("somesh.22", "someshSINGH@22")

# Read CSV
scrape_csv = pd.read_csv(CSV_PATH)
scrape_csv = scrape_csv[3000:].drop_duplicates()
f = open("scrapes.txt", "w+")

# Scraping Loop
locations = scrape_csv["Apartment Name"] + " " + scrape_csv["City"]
links = []
for i, location in enumerate(locations):
    try:
        scrape_bot.search(location)
        links.append(scrape_bot.get_locs())
        if len(links) > 1 and links[-1] == links[-2]:
            time.sleep(2)
            links[-1] = scrape_bot.get_locs()
        f.write(links[-1])
        f.write("\n")
    except:
        links.append("NOT FOUND")
        f.write("NOT FOUND\n")
    print(str(i + 1) + links[-1].split(",")[0])

# Save Results
scrape_csv["Links"] = links
scrape_csv.to_csv("insta_locs.csv", index=False)
scrape_bot.end()
