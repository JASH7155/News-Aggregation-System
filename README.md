⭐ README.md — News Aggregation System
📰 News Aggregation System

An automated, end-to-end news pipeline that fetches, normalizes, stores, and serves real-time news across multiple categories.
Built with Python, Flask, MySQL, HTML/CSS/JS, and a scheduled background processor.

🚀 Features
🔥 Automated News Fetching

Fetches 200+ news articles across 4 categories:

General

Technology

Business

Sports

Uses NewsAPI /everything endpoint

Normalizes 7+ fields (title, description, URL, image, source, category, timestamp)

Deduplicates articles using unique URL constraints

⚙️ Data Pipeline & Storage

MySQL-backed storage

URL-based deduplication

Clean table schema with indexing

Stores articles in a structured format for fast retrieval

🖥️ Dynamic Frontend UI

Modern card layout with images, descriptions, timestamps

Category filter & Search bar

“Load More” functionality

Relative timestamps like “2h ago”

Lazy-loading images (improves performance)

Responsive layout for mobile & desktop

🤖 Recommendation Engine

Simple content-based recommendation (title/description similarity)

Category preference boosting

Recency-weighted scoring

Displayed as a sidebar in the UI

⏱️ Background Scheduler

Runs every 10 minutes

Fetches new data

Inserts into MySQL

Regenerates static UI page

Logs every cycle into logs/scheduler.log

🌐 Local API Server

Powered by Flask:

Endpoint	Description
/api/latest	Returns latest articles from MySQL
/api/refresh	Triggers background fetch & DB update
/api/recommend	Returns recommended articles
/	Serves the UI frontend
🧱 Project Structure
news_aggregator/
│
├── src/
│   ├── config.py           # Load .env settings
│   ├── db.py               # MySQL connection + queries
│   ├── fetch_news.py       # Fetch & normalize news
│   ├── normalizer.py       # Clean article normalization logic
│   ├── generate_html.py    # Build the frontend index.html
│   ├── scheduler.py        # Automated scheduled job
│   └── server.py           # Flask API server
│
├── templates/
│   └── index_template.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── output/
│   └── index.html          # Generated UI
│
├── logs/
│   └── scheduler.log
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

🛠️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/JASH7155/News-Aggregation-System
cd News-Aggregation-System

2️⃣ Create & Activate Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate


Mac/Linux:

python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Copy .env.example → .env and add your details:

NEWSAPI_KEY=YOUR_KEY
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_password
DB_NAME=newsdb

5️⃣ Create MySQL Database

Run inside MySQL Workbench or CLI:

CREATE DATABASE IF NOT EXISTS newsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE newsdb;

CREATE TABLE IF NOT EXISTS articles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(300),
  description TEXT,
  url VARCHAR(500) UNIQUE,
  source VARCHAR(100),
  category VARCHAR(50),
  published_at DATETIME,
  image_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_category (category),
  INDEX idx_published_at (published_at)
);

▶️ Running the Project
🔹 Run backend API server
python src/server.py


Open browser:

http://127.0.0.1:5000


The UI will:

Fetch latest data from /api/latest

Show recommendations

Allow filters, search, and load more

🔹 Run the Scheduler
python src/scheduler.py


Runs every 10 minutes and updates the system automatically.

🔹 Run manual data fetch
python src/fetch_news.py

🔹 Regenerate UI HTML
python src/generate_html.py

🎨 UI Highlights
✓ Modern card layout
✓ Lazy-loaded thumbnails
✓ “Load More” pagination
✓ Category filter & search
✓ Recommendations sidebar
✓ Fully responsive
🧠 Recommendation Algorithm (Simple, Explainable)

Extracts keywords from title + description

Computes overlap score

Adds category bonus

Adds recency bonus

Returns top-N articles

This makes the recommendation logic transparent and discussable in interviews.

📦 Future Improvements (Interview Talking Points)

TF-IDF or embedding-based recommendation

Redis caching for /api/latest

Queue-based job runner (Celery / RQ)

Dockerized deployment

CI/CD with GitHub Actions

Authentication for /api/refresh

Deploy server on Render/Heroku

📸 Screenshots (Add yours here)
screenshots/
 ├── homepage.png
 ├── recommendations.png
 ├── scheduler.png
 └── mysql.png


Example:

### Homepage
![Homepage](screenshots/homepage.png)

📝 License

MIT License