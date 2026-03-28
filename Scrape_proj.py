import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_quotes(pages=3):
    base_url = "http://quotes.toscrape.com/page/{}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    data_list = []

    for page in range(1, pages + 1):
        url = base_url.format(page)
        print(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            quotes = soup.find_all("div", class_="quote")
            if not quotes:
                print(f"No quotes found on page {page}")
                break

            for quote in quotes:
                text = quote.find("span", class_="text").get_text(strip=True)
                author = quote.find("small", class_="author").get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

                data_list.append({
                    "Quote": text,
                    "Author": author,
                    "Tags": ", ".join(tags)
                })

            time.sleep(1)  

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    if data_list:
        df = pd.DataFrame(data_list)
        df.drop_duplicates(inplace=True)
        return df
    else:
        return pd.DataFrame()  
df = scrape_quotes(pages=5) 

if not df.empty:
    df.to_csv("quotes_scraped.csv", index=False)
    df.to_excel("quotes_scraped.xlsx", index=False)
    print(f"\n✅ Scraping complete! {len(df)} quotes saved to CSV & Excel")
else:
    print("❌ No data scraped")