import requests
from bs4 import BeautifulSoup

URLS = [
    "https://debales.ai/",
]

def scrape_website():
    all_text = []

    for url in URLS:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator=" ", strip=True)
            all_text.append(text)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return all_text