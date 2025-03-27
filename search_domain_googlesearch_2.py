import pandas as pd
from googlesearch import search
import time

MAX_RETRIES = 3
SLEEP_TIME = 5  # Increase to avoid rate limiting

def get_domain_from_google(company_name):
    query = f"{company_name} official site"
    try:
        for result in search(query, num_results=5):
            if result.startswith("http"):
                return result
        return "No valid result"
    except Exception as e:
        return f"Error: {str(e)}"

def lookup_with_retries(company_name):
    for attempt in range(MAX_RETRIES):
        result = get_domain_from_google(company_name)
        if result.startswith("http"):
            return result
        time.sleep(SLEEP_TIME)  # wait between retries
    return "Failed after retries"

# Load Excel
df = pd.read_excel("C:/Users/Andrei/Downloads/company_names.xlsx")
company_names = df["Company Name"]

# Result storage
domains = []
failures = []

# First pass
for name in company_names:
    print(f"Searching for: {name}")
    domain = lookup_with_retries(name)
    domains.append(domain)
    if not domain.startswith("http"):
        failures.append(name)
    time.sleep(SLEEP_TIME)

# Save to DataFrame
df["Domain"] = domains
df.to_excel("C:/Users/Andrei/Downloads/companies_with_domains.xlsx", index=False)

# Optional: Save failures to a separate file
if failures:
    pd.DataFrame(failures, columns=["Company Name"]).to_excel("failed_lookups.xlsx", index=False)
    print(f"\n{len(failures)} companies failed after {MAX_RETRIES} retries. Saved to 'failed_lookups.xlsx'.")
else:
    print("\nAll companies resolved successfully!")