# 📰 News Aggregation System

A fully automated news aggregation pipeline that fetches, normalizes, stores, and serves real-time news across multiple categories. Includes a dynamic frontend, a recommendation engine, a background scheduler, and a local Flask API server.

Built with **Python, Flask, MySQL, HTML/CSS/JS**.

---

## 🚀 Features

### 🔥 Automated News Fetching

* Fetches **200+ news articles** every cycle using NewsAPI
* Supports **4 categories**: General, Technology, Business, Sports
* Normalizes **7+ fields**
* URL-based duplicate prevention

### ⚙️ Data Pipeline & Storage

* Stores normalized news data in **MySQL**
* Clean schema with indexes
* Fast retrieval & safe inserts

### 🖥️ Dynamic Frontend UI

* Modern responsive card layout
* Category filter & search
* **Load More** button
* Lazy-loaded images
* **Relative timestamps** (e.g., “2h ago”)
* Recommendation sidebar

### 🤖 Recommendation Engine

Simple & explainable:

* Title + description similarity
* Category preference
* Recency boost
* Returns top 6 recommended articles

### ⏱️ Automated Scheduler

Runs every **10 minutes**:

* Fetches new data
* Updates MySQL
* Regenerates UI
* Logs stored in `logs/scheduler.log`

### 🌐 Flask API Server

| Endpoint         | Description                |
| ---------------- | -------------------------- |
| `/api/latest`    | Returns latest articles    |
| `/api/refresh`   | Triggers fetch + DB update |
| `/api/recommend` | Returns recommendations    |
| `/`              | Serves frontend            |

---

## 🧱 Project Structure

```
news_aggregator/
├── src/
│   ├── config.py
│   ├── db.py
│   ├── fetch_news.py
│   ├── normalizer.py
│   ├── generate_html.py
│   ├── scheduler.py
│   └── server.py
│
├── templates/
│   └── index_template.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── output/
│   └── index.html
│
├── logs/
│   └── scheduler.log
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/JASH7155/News-Aggregation-System
cd News-Aggregation-System
```

### 2️⃣ Create Virtual Environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Environment Variables

Create `.env` (based on `.env.example`):

```
NEWSAPI_KEY=YOUR_NEWS_API_KEY
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_password
DB_NAME=newsdb
```

### 5️⃣ MySQL Database Setup

```
CREATE DATABASE IF NOT EXISTS newsdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE newsdb;

CREATE TABLE articles (
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
```

---

## ▶️ Running the Project

### 🔹 Run API Server

```
python src/server.py
```

Open browser:

```
http://127.0.0.1:5000
```

### 🔹 Start Scheduler

```
python src/scheduler.py
```

### 🔹 Manually Fetch Articles

```
python src/fetch_news.py
```

### 🔹 Regenerate UI

```
python src/generate_html.py
```

---

## 🎨 UI Highlights

* Category filtering
* Search bar
* Load More button
* Lazy image loading
* Responsive card design
* Recommendation sidebar
* Clean user experience

---

## 🧠 Recommendation Logic

Each recommendation is ranked using:

1. Word overlap between titles/descriptions
2. Category match
3. Recent articles boosted
4. Top 6 articles returned

---

## 🧩 Future Enhancements

* Better recommendation model (TF-IDF / embeddings)
* Redis caching for API
* Docker containerization
* Cloud deployment
* CI/CD via GitHub Actions
* User preference tracking

---

## 📸 Screenshots (Add yours)

Create a folder:

```
screenshots/
  homepage.png
  recommendations.png
  scheduler.png
  mysql.png
```

Example markdown:

```
### Homepage
![Homepage](screenshots/homepage.png)
```

---

## 📝 License

MIT License

---

## 👤 Author

**Sai Jashwanth Pantham**

CMR Engineering College

GitHub: [https://github.com/JASH7155](https://github.com/JASH7155)


