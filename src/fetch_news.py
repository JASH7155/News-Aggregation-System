# src/fetch_news.py
import os
import time
import requests
from dotenv import load_dotenv
from db import insert_article
from normalizer import normalize_newsapi_item

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# We'll use the /everything endpoint with a query per category
# Each category is mapped to a search keyword (simple approach)
CATEGORIES = {
    "general": "india",
    "technology": "technology",
    "business": "business",
    "sports": "sports"
}

# pageSize per request
PAGE_SIZE = 50

NEWSAPI_URL_TEMPLATE = "https://newsapi.org/v2/everything?q={query}&language=en&pageSize={pageSize}&apiKey={key}"

def fetch_category_and_store(cat_key, query):
    url = NEWSAPI_URL_TEMPLATE.format(query=query, pageSize=PAGE_SIZE, key=NEWSAPI_KEY)
    print(f"Fetching category='{cat_key}' using query='{query}'")
    try:
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        print("HTTP error for category", cat_key, ":", e)
        return 0

    data = resp.json()
    articles = data.get("articles", [])
    print(f"  Fetched {len(articles)} articles for {cat_key}")

    inserted = 0
    for item in articles:
        normalized = normalize_newsapi_item(item, category_hint=cat_key)
        ok = insert_article(normalized)
        if ok:
            inserted += 1

    print(f"  Inserted {inserted} articles for {cat_key}")
    return inserted

def fetch_all_categories():
    if not NEWSAPI_KEY:
        print("NEWSAPI_KEY missing in .env")
        return

    total_inserted = 0
    for cat, query in CATEGORIES.items():
        inserted = fetch_category_and_store(cat, query)
        total_inserted += inserted
        # small pause to avoid rate limit issues on free plans
        time.sleep(1.5)
    print(f"Done. Total inserted across categories: {total_inserted}")

if __name__ == "__main__":
    fetch_all_categories()
