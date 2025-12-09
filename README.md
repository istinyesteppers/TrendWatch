# TrendWatch
🕵️‍♂️ TrendWatch
Multi-Source Trend Monitoring Tool

A Python project for scraping, storing, and analyzing trending data.

📌 Overview

TrendWatch is a modular trend-monitoring system that collects trending topics from multiple platforms (currently Reddit + YouTube) and stores them in a database for later viewing.

The system is designed using clean Object-Oriented Programming (OOP) principles and supports two database backends:

SQLite (default) → simple, portable, professor-friendly

MongoDB (optional) → advanced, flexible, used for bonus features

🚀 Features
🔍 Web Scraping + APIs

Reddit trending posts (via JSON API)

YouTube Trending videos (BeautifulSoup web scraper)

Unified data format using a shared TrendItem model

🧠 OOP Architecture

BaseTrendSource → abstract parent class

RedditTrendSource & YouTubeTrendSource inherit from it

TrendMonitor controls the full fetch → save → display flow

Modular design → easily add more platforms later

🗃 Dual Database Support
Database	Purpose
SQLite	Default storage. No setup needed. Perfect for evaluation.
MongoDB	Optional backend for advanced users. More flexible, real-world usage.

Switching databases requires changing one line:

USE_MONGO = True   # or False

🧩 Project Structure
TrendWatch/
│
├── main.py               # CLI app & DB switching
├── base_source.py        # Abstract base class for all sources
├── reddit_source.py      # Reddit scraper
├── youtube_source.py     # YouTube trending scraper
├── models.py             # TrendItem data model
├── monitor.py            # Coordinates scraping + saving + output
├── db.py                 # SQLite database backend
├── mongo_db.py           # MongoDB backend (optional)
└── trends.db             # SQLite database file

📦 Installation
1. Install required Python packages
py -m pip install requests beautifulsoup4 lxml pymongo


Only requests + bs4 are required for SQLite mode.
pymongo is only needed if MongoDB mode is enabled.

🧰 Running the Program
Default (SQLite mode)
py main.py

Inside the app
=== TrendWatch ===
1) Fetch & store new trends
2) Show latest stored trends
3) Exit

🗄 Enabling MongoDB (optional)

In main.py:

USE_MONGO = True


MongoDB becomes the storage engine automatically.

SQLite remains the default to ensure the project runs on any system.

🧠 How It Works (Simplified)

User selects data source (Reddit / YouTube).

Scraper collects top trending items.

TrendMonitor validates the data.

Data is saved into either SQLite or MongoDB.

User can view the latest saved trends at any time.

🔮 Future Improvements

Add Twitter/X trending

Add TikTok trending

Auto-scrape every hour (scheduler)

Export results to CSV/JSON

Build a web dashboard for visualization

🎓 Why This Project Stands Out

Clean OOP design

Multiple scrapers

Real-world DB flexibility

Easy to extend

Professor can run it with zero setup

Extra credit features available