# src/normalizer.py
from datetime import datetime

def parse_iso_datetime(s):
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except Exception:
        return None

def normalize_newsapi_item(item, category_hint="general"):
    """
    Normalize a raw NewsAPI item into our article schema.
    Returns dict with keys:
      title, description, url, source, category, published_at, image_url
    """
    title = (item.get("title") or "").strip()
    description = (item.get("description") or "").strip()
    url = item.get("url")
    source = (item.get("source") or {}).get("name")
    # Use provided category hint (from our query) as canonical category
    category = category_hint or "general"
    published_at = parse_iso_datetime(item.get("publishedAt"))
    # in src/normalizer.py, adjust image_url line
    raw_image = item.get("urlToImage")
    image_url = raw_image[:1000] if raw_image else None


    return {
        "title": title[:300] if title else None,
        "description": description or None,
        "url": url,
        "source": source or None,
        "category": category,
        "published_at": published_at,
        "image_url": image_url or None,
    }
