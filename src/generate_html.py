# src/generate_html.py
import os
from pathlib import Path
from db import fetch_latest

BASE = Path(__file__).resolve().parent.parent
TEMPLATE = BASE / "templates" / "index_template.html"
OUTPUT_DIR = BASE / "output"
OUTPUT_FILE = OUTPUT_DIR / "index.html"

def make_card_html(article):
    # safe extraction and escape minimal chars
    title = article.get("title") or "No title"
    desc = article.get("description") or ""
    url = article.get("url") or "#"
    img = article.get("image_url") or ""
    source = article.get("source") or "Unknown"
    category = article.get("category") or "general"
    pub = article.get("published_at")
    if hasattr(pub, "isoformat"):
        pub = pub.isoformat()
    card = f"""
    <article class="card" data-title="{escape_attr(title)}" data-desc="{escape_attr(desc)}" data-category="{category}">
      <img loading="lazy" src="{escape_attr(img)}" alt="{escape_attr(title)}">
      <div class="card-body">
        <div class="title">{escape_html(title)}</div>
        <div class="meta">{escape_html(source)} • {escape_html(pub or '')}</div>
        <div class="desc">{escape_html(desc)}</div>
        <a class="link" href="{escape_attr(url)}" target="_blank" rel="noopener noreferrer">Read more</a>
      </div>
    </article>
    """
    return card

def escape_html(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def escape_attr(s):
    return escape_html(s).replace('"', "&quot;")

def generate(limit=20):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()

    articles = fetch_latest(limit=limit)
    cards = [make_card_html(a) for a in articles]
    cards_html = "\n".join(cards)

    out = tpl.replace("<!-- NEWS_CARDS_PLACEHOLDER -->", cards_html)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Generated {OUTPUT_FILE} with {len(cards)} articles.")

if __name__ == "__main__":
    generate(20)
