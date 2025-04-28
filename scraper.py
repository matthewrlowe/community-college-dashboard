import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import time
import random

# Search terms you wantscraper
search_queries = [
    "community college get started site:.edu",
    "community college toolkit site:.edu",
    "community college enrollment steps site:.edu",
    "community college new student guide site:.edu"
]

# How many pages deep to scrape per query
pages_to_scrape = 3

# Storage for all found links
all_links = []

# Headers to act like a human browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

for query in search_queries:
    print(f"🔎 Searching for: {query}")

    # Encode query for URL
    encoded_query = urllib.parse.quote_plus(query)

    for page in range(pages_to_scrape):
        print(f"📄 Scraping page {page + 1}")

        # DuckDuckGo search URL
        search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}&s={page * 50}"

        try:
            # Send request
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all result links
            for result in soup.find_all('a', class_='result__a', href=True):
                title = result.get_text(strip=True)
                link = result['href']

                # Clean up DuckDuckGo redirect links
                clean_link = urllib.parse.unquote(link.split('uddg=')[-1])

                # Only keep .edu links
                if ".edu" in clean_link:
                    all_links.append({
                        'search_query': query,
                        'college_name': title,
                        'link': clean_link
                    })

            # Random delay between pages (be polite)
            time.sleep(random.uniform(1.5, 3.5))

        except Exception as e:
            print(f"❌ Error scraping page {page + 1} of query '{query}': {e}")

print(f"✅ Found {len(all_links)} total results!")

# Save to CSV
df = pd.DataFrame(all_links)
df.to_csv('multi_search_college_links.csv', index=False)

print("🎯 All results saved to 'multi_search_college_links.csv'")
