# pip install requests beautifulsoup4 tldextract

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
import time

def is_valid_link(href, base_url):
    if not href:
        return False
    parsed = urlparse(href)
    if parsed.scheme not in ["http", "https", ""]:
        return False
    if href.endswith(('.jpg', '.jpeg', '.png', '.pdf', '.zip', '.exe')):
        return False
    return tldextract.extract(href).registered_domain == tldextract.extract(base_url).registered_domain

def get_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return text

def crawl_website(base_url, max_pages=10):
    visited = set()
    to_visit = [base_url]
    collected_text = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✔ Crawled: {url}")
                visited.add(url)
                page_text = get_visible_text(response.text)
                collected_text.append(page_text)

                soup = BeautifulSoup(response.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    full_url = urljoin(url, a['href'])
                    if is_valid_link(full_url, base_url) and full_url not in visited:
                        to_visit.append(full_url)
            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")

    return collected_text

domain = "https://codewave.com/"
all_texts = crawl_website(domain, max_pages=30)

# Optional: print or save to a file
for i, text in enumerate(all_texts):
    print(f"\n--- Page {i+1} ---\n{text[:500]}...")  # Show only the first 500 characters


with open("C:/Users/Andrei/Downloads/microsoft_text.txt", "w", encoding="utf-8") as f:
    for i, page_text in enumerate(all_texts):
        f.write(f"\n--- Page {i+1} ---\n")
        f.write(page_text)
        f.write("\n\n")