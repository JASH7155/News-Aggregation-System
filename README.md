# News Aggregation System

**Simple end-to-end News Aggregator** — Python + MySQL + static HTML UI.  
Fetches news from multiple categories, normalizes and stores articles, and generates a static HTML page you can open locally.

---

## Features
- Fetches news from NewsAPI for 4 categories: `general`, `technology`, `business`, `sports`
- Normalizes 7+ fields: `title`, `description`, `url`, `image_url`, `source`, `category`, `published_at`
- Stores articles in MySQL with duplicate prevention (URL unique)
- Generates a static, responsive HTML page: `output/index.html`
- Simple scheduler to run fetch + html generation every 10 minutes
- Minimal dependencies; no web frameworks required

---

## Tech Stack
- Python 3.10+
- MySQL
- requests, python-dotenv, mysql-connector-python, schedule, Jinja2 (optional)
- Simple HTML/CSS/JS for frontend

---

## Repo Structure
