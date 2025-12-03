# src/server.py
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import threading
import time

# reuse your modules
from fetch_news import fetch_all_categories
from db import fetch_latest, get_connection

BASE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "output"
TEMPLATE_PATH = BASE / "templates"
STATIC_DIR = BASE / "static"

app = Flask(__name__, static_folder=str(STATIC_DIR), template_folder=str(TEMPLATE_PATH))

# API: get latest articles (JSON)
@app.route("/api/latest")
def api_latest():
    try:
        limit = int(request.args.get("limit", 20))
    except:
        limit = 20
    category = request.args.get("category")  # optional
    articles = fetch_latest(limit=limit, category=category)
    # normalize datetimes to iso strings
    for a in articles:
        if isinstance(a.get("published_at"), (str,)):
            pass
        elif a.get("published_at") is None:
            a["published_at"] = ""
        else:
            try:
                a["published_at"] = a["published_at"].isoformat()
            except:
                a["published_at"] = str(a.get("published_at"))
    return jsonify({"articles": articles})

# API: refresh / fetch latest from NewsAPI (runs fetch_all_categories())
# This is synchronous and can take a few seconds. For safety, restrict to local.
@app.route("/api/refresh", methods=["POST", "GET"])
def api_refresh():
    # optional: protect with a simple token in .env if you want
    # run fetch_all_categories() in a background thread to return quickly
    def run_fetch():
        try:
            fetch_all_categories()
        except Exception as e:
            app.logger.exception("Background fetch failed: %s", e)

    t = threading.Thread(target=run_fetch, daemon=True)
    t.start()
    return jsonify({"status": "started", "message": "Fetching in background. Please wait a few seconds and call /api/latest."})

# API: recommend articles
# Simple content-based recommender: returns top N articles similar to recent ones or to an article id
@app.route("/api/recommend")
def api_recommend():
    # parameters:
    #  - article_id (optional): recommend similar to this article
    #  - category (optional): prefer this category
    try:
        limit = int(request.args.get("limit", 6))
    except:
        limit = 6
    article_id = request.args.get("article_id")
    category_pref = request.args.get("category")

    # fetch top 200 latest articles for computing recs
    all_articles = fetch_latest(limit=200, category=None)

    # helper: simple tokenizer -> set of lowercase words
    def toks(s):
        if not s:
            return set()
        return set([w.strip(".,:;\"'()[]{}").lower() for w in s.split() if len(w) > 2])

    # if article_id provided, find that article
    base_tokens = set()
    base_category = None
    if article_id:
        for a in all_articles:
            if str(a.get("id")) == str(article_id):
                base_tokens = toks(a.get("title") or "") | toks(a.get("description") or "")
                base_category = a.get("category")
                break

    # scoring: token overlap + category bonus + recency (published_at)
    scored = []
    from datetime import datetime
    for a in all_articles:
        score = 0
        title_desc = (a.get("title") or "") + " " + (a.get("description") or "")
        words = toks(title_desc)
        # token overlap
        if base_tokens:
            overlap = len(base_tokens & words)
            score += overlap * 3
        # category preference
        if category_pref and a.get("category") == category_pref:
            score += 4
        if base_category and a.get("category") == base_category:
            score += 2
        # boost for recent items
        pub = a.get("published_at")
        if isinstance(pub, str) and pub:
            try:
                dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                age_secs = (datetime.utcnow() - dt).total_seconds()
                # less age => higher score
                score += max(0, 5 - (age_secs / 3600 / 24))  # small decay
            except:
                pass
        # add small base score to avoid zeros
        score += 0.01
        scored.append((score, a))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [a for s, a in scored[:limit]]
    # ensure published_at is string
    for a in top:
        if hasattr(a.get("published_at"), "isoformat"):
            a["published_at"] = a["published_at"].isoformat()
    return jsonify({"recommendations": top})

# Serve the generated output HTML (so you can still open index.html)
@app.route("/")
def index():
    return send_from_directory(str(OUTPUT_DIR), "index.html")

# Serve static files (css/js)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(str(STATIC_DIR), filename)

if __name__ == "__main__":
    # run only on localhost for safety
    app.run(host="127.0.0.1", port=5000, debug=False)
