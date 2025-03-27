# Automation Project: AI-Powered ESG Insights from Corporate Websites



## 📌 Project Overview

This Automation Project is an advanced data extraction and analysis pipeline designed to automate the process of retrieving ESG (Environmental, Social, and Governance) information from company websites. By leveraging web scraping, NLP embedding, vector search, and AI-powered query processing, this project enables efficient ESG intelligence gathering from publicly available sources.

This project is particularly valuable for ESG analysts, investment firms, and sustainability researchers who require streamlined access to ESG-related disclosures without manual data collection.

---

## 🚀 Features

- **Automated Domain Discovery**: Uses Google Search to find official domains of companies.
- **Web Scraping & Crawling**: Extracts textual data from company websites.
- **Text Processing & Vector Storage**: Splits, embeds, and stores extracted text in FAISS (Facebook AI Similarity Search) for efficient querying.
- **AI-Driven ESG Analysis**: Queries an LLM (Ollama’s Mistral model) to extract insights on Environmental, Social, and Governance aspects of each company.
- **Structured Output**: Generates ESG reports in JSON and CSV formats for easy analysis and further processing.

---

## 🔬 How It Works

### 1️⃣ **Company Name to Domain Lookup**

- The system takes an input Excel file (`company_names.xlsx`) containing company names.
- Using the Google Search API, it finds the most relevant official website for each company.
- Results are stored in an updated Excel file (`companies_with_domains.xlsx`).

### 2️⃣ **Website Crawling & Text Extraction**

- The script scrapes the website’s visible text, ignoring scripts, styles, and unnecessary data.
- It follows internal links up to a predefined depth to gather comprehensive textual content.

### 3️⃣ **Text Preprocessing & Vectorization**

- Extracted text is split into manageable chunks (1000 characters with 200 overlap) to maintain context.
- The chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2` and stored in FAISS for efficient similarity search.

### 4️⃣ **AI-Powered ESG Querying**

- A retrieval-based QA system is used to extract ESG-specific insights.
- The system poses predefined questions related to ESG aspects and retrieves the most relevant information using a local LLM model (`mistral`).

### 5️⃣ **Data Output**

- The final ESG analysis is stored in `esg_combined_report.json` and `esg_combined_report.csv`.

---

## 🛠️ Setup & Installation

### 1️⃣ **Install Dependencies**

Ensure you have Python 3.8+ installed, then install the required packages:

```bash
pip install pandas requests beautifulsoup4 googlesearch-python faiss-cpu langchain tldextract
```

### 2️⃣ **Run the Domain Lookup**

```bash
python search_domain_googlesearch_2.py
```

### 3️⃣ **Run the Web Scraper**

```bash
python web_scrapping.py
```

### 4️⃣ **Process ESG Data**

```bash
python esg_langchain_full.py
```

---

## 📖 Theoretical Background

### 🌿 **What is ESG?**

Environmental, Social, and Governance (ESG) criteria are used to evaluate a company's commitment to sustainable and ethical business practices. ESG intelligence is crucial for investors, regulators, and stakeholders to assess corporate responsibility and risk.

### 🔍 **Why Use AI for ESG Analysis?**

- **Scalability**: Manually extracting ESG insights from corporate disclosures is time-consuming.
- **Objectivity**: AI reduces bias by relying on factual text processing.
- **Efficiency**: Automates text retrieval, structuring, and analysis, reducing manual workload.

### 🤖 **Technical Components**

- **Natural Language Processing (NLP)**: Processes textual data from websites.
- **FAISS Vector Database**: Enables quick retrieval of relevant text chunks.
- **LLM-Based Querying**: Uses Mistral to provide AI-driven ESG insights.

---

## 📈 Applications

- **Sustainability & ESG Research**
- **Investment & Risk Analysis**
- **Regulatory Compliance Monitoring**

---

## 🏆 Why This Project Stands Out

- **Fully Automated Workflow**: From domain discovery to ESG analysis.
- **AI-Powered**: Combines NLP, vector search, and LLM querying.
- **Scalable & Extensible**: Can be expanded to analyze multiple sectors and geographies.

---

## 📌 Conclusion

ESG Intel automates the process of collecting and analyzing ESG-related information from corporate websites, significantly reducing manual effort and improving the accuracy of ESG assessments.

For further enhancements, the model can be fine-tuned with additional ESG-related text data, and new AI models can be integrated for even more precise ESG intelligence extraction.

---

## 📮 Contact & Contributions

Feel free to contribute or reach out for collaborations!

