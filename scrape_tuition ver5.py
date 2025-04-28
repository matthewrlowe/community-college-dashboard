import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of keywords you want to search for
keywords = ["toolkit", "get started", "new to community college", "getting started", "advocacy", "advocacy toolkit", "advocacy resources", "advocacy tools", "advocacy guide", "advocacy guide toolkit", "advocacy guide resources", "advocacy guide tools"]

# List of URLs to scrape
urls = [
    'https://www.ed.gov/',  
    'https://www.aacc.nche.edu/',              
    'https://educationusa.state.gov/',
    'https://www.nacacnet.org/',
    'https://www.acenet.edu/',
    'https://www.acct.org/',
    # You can add 10, 20, 100+ more
]

# Where to store results
all_matches = []

# Go through each URL
for url in urls:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        matches = []

        # FIRST: Look inside links (<a> tags)
        for link in soup.find_all('a'):
            link_text = link.get_text(strip=True)
            href = link.get('href')

            for keyword in keywords:
                if keyword.lower() in link_text.lower():
                    # Make sure the link is complete
                    if href and not href.startswith('http'):
                        href = requests.compat.urljoin(url, href)
                    matches.append({
                        'matched_text': link_text,
                        'link_url': href
                    })

        # SECOND: Look inside plain text (like <p>, <div>, etc.)
        for element in soup.find_all(text=True):
            clean_text = element.strip()
            if not clean_text:
                continue  # Skip empty text

            parent = element.parent  # Check the HTML element the text is inside

            for keyword in keywords:
                if keyword.lower() in clean_text.lower():
                    # Try to find a nearby link
                    link_tag = parent.find('a')
                    if link_tag and link_tag.get('href'):
                        nearby_link = link_tag.get('href')
                        if not nearby_link.startswith('http'):
                            nearby_link = requests.compat.urljoin(url, nearby_link)
                    else:
                        nearby_link = 'N/A'

                    matches.append({
                        'matched_text': clean_text,
                        'link_url': nearby_link
                    })

        if not matches:
            matches.append({
                'matched_text': 'No matching keywords found',
                'link_url': 'N/A'
            })

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        matches = [{
            'matched_text': 'Scraping failed',
            'link_url': 'N/A'
        }]

    # Save results for this page
    for match in matches:
        all_matches.append({
            'page_url': url,
            'matched_text': match['matched_text'],
            'link_url': match['link_url']
        })

# Save everything to CSV
df = pd.DataFrame(all_matches)
df.to_csv('supercharged_keyword_links.csv', index=False)

print("✅ Supercharged scraping completed! Data saved to 'supercharged_keyword_links.csv'.")
