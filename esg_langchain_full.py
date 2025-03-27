from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
#from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import pandas as pd
import json
import os

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

# ESG questions
esg_questions = {
    "Environmental": "What information is available about the company's environmental practices, sustainability, emissions, or green initiatives?",
    "Social": "What information is available about the company's social responsibility, employee treatment, diversity, or community engagement?",
    "Governance": "What information is available about the company's governance, leadership structure, ethics, or compliance?"
}

# Load Excel file with company names and domains
df = pd.read_excel("C:/Users/Andrei/Downloads/companies_with_domains_3.xlsx")

# Create output directory
os.makedirs("esg_text_chunks", exist_ok=True)

# Embedding model (local)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Local LLM from Ollama
llm = Ollama(model="mistral")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Store ESG output
esg_report = []

for index, row in df.iterrows():
    company = row["Company Name"]
    domain = row["Domain"]

    if not isinstance(domain, str) or not domain.startswith("http"):
        continue

    print(f"\n🌍 Processing {company} - {domain}")
    try:
        # Step 1: Crawl website
        texts = crawl_website(domain, max_pages=5)
        if not texts:
            continue

        # Step 2: Chunk text
        combined_text = " ".join(texts)
        chunks = text_splitter.split_text(combined_text)

        # Optional: Save raw chunks
        with open(f"esg_text_chunks/{company.replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(chunk + "\n\n")

        # Step 3: Embed & store in FAISS
        vectorstore = FAISS.from_texts(chunks, embedding_model)
        retriever = vectorstore.as_retriever()

        # Step 4: Ask ESG questions
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )

        esg_entry = {"company": company}
        for category, question in esg_questions.items():
            print(f"🔍 {company} - {category}")
            answer = qa.run(question)
            esg_entry[category] = answer

        esg_report.append(esg_entry)

    except Exception as e:
        print(f"❌ Error processing {company}: {e}")

# Save final ESG report
with open("esg_combined_report.json", "w", encoding="utf-8") as f:
    json.dump(esg_report, f, indent=4)

pd.DataFrame(esg_report).to_csv("esg_combined_report.csv", index=False)
print("\n✅ ESG extraction complete! Saved JSON and CSV reports.")