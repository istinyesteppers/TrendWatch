````markdown
# TrendWatch 🕵️‍♂️  
Multi-Source Trend Monitoring Tool

A Python project for scraping, storing, and inspecting trending data from multiple sources using clean OOP and real databases.

This combines the **Web Monitoring (Project 2)** and **Database App (Project 3)** ideas into a single system.

---

## 🔍 Project Idea

**TrendWatch** is a console app that:

1. Fetches “trending” items from different sources  
   - Reddit JSON API  
   - Web scraping (Hacker News via Scrapy)  
   - YouTube demo source (for polymorphism / OOP)  
2. Saves them to a database (SQLite or MongoDB)  
3. Lets the user view the latest saved trends from a simple CLI menu.

It is designed to show:

- Web scraping / APIs  
- Databases  
- OOP and separation of concerns  
- Basic robustness and testing

---

## 🧱 Architecture Overview

### Core model

**`models.py`**

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Platform = Literal["reddit", "youtube", "web"]

@dataclass
class TrendItem:
    """Represents a single trending item from any platform."""
    platform: Platform
    title: str
    url: str
    score: int
    rank: int
    fetched_at: datetime
````

All data flows through this dataclass, no matter which source or database is used.

---

### Source abstraction (scraping / APIs)

**`base_source.py`**

```python
from abc import ABC, abstractmethod
from typing import List
from models import TrendItem

class BaseTrendSource(ABC):
    """Abstract base for all trend sources."""

    @abstractmethod
    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        """Return a list of TrendItem objects."""
        raise NotImplementedError
```

All concrete sources implement `fetch_trends(limit)`:

* **`RedditTrendSource` (`reddit_source.py`)**

  * Uses `requests` to hit the Reddit JSON API
  * Fetches top posts from a subreddit
  * Converts each post to `TrendItem`

* **`ScrapyHNSource` (`scrapy_source.py`)**

  * Uses a Scrapy spider to scrape the Hacker News front page
  * Extracts title, URL, rank
  * Returns them as `TrendItem` (`platform="web"`)

* **`YouTubeTrendSource` (`youtube_source.py`)**

  * Demo source generating fake “Trending YouTube Video #N (REGION)” items
  * Used for polymorphism and robustness testing
  * Handles bad parameters safely

---

### Database backends

Two interchangeable backends implement the same conceptual interface:

* **SQLite backend – `TrendDatabase` (`db.py`)**

  * Uses Python’s built-in `sqlite3`
  * Creates `trends` table
  * `save_trends()` and `get_latest()`
  * Wrapped in try/except for robustness

* **MongoDB backend – `MongoTrendDB` (`mongo_db.py`)**

  * Uses `pymongo`
  * Stores each trend as a document
  * Safe ISO timestamp parsing
  * Also provides `save_trends()` and `get_latest()`

---

### Business logic

**`monitor.py`**

```python
class TrendMonitor:
    """Coordinates fetching trends from a source and saving them to a database."""

    def __init__(self, source: BaseTrendSource, db):
        self.source = source
        self.db = db

    def fetch_and_store(self, limit: int = 10) -> None:
        """Fetch trends from the source and store them safely."""
        ...

    def show_latest(self, limit: int = 10) -> None:
        """Print the latest saved trends in a readable format."""
        ...
```

* Decouples scraping logic from database logic
* Handles empty responses and exceptions
* Prints formatted trend output

---

### CLI entry point

**`main.py`** provides the terminal interface:

* Choose **database backend** (SQLite or MongoDB)
* Choose **source** (Reddit / YouTube / Web via Scrapy)
* Fetch & store new trends
* Show latest trends
* Switch backend at runtime

Menu example:

```text
=== TrendWatch ===
(Current DB: SQLite or MongoDB)
1) Fetch & store new trends
2) Show latest saved trends
3) Exit
4) Switch database backend
Choose option:
```

---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/istinyesteppers/TrendWatch.git
cd TrendWatch
```

### 2. Install dependencies

```bash
py -m pip install requests pymongo scrapy
```

### 3. (Optional) MongoDB setup

If using MongoDB:

* Install MongoDB Community Server or run via Docker
* Ensure it runs at: `mongodb://localhost:27017`

SQLite works out of the box.

---

## 🚀 Running the App

Start the program:

```bash
py main.py
```

Then follow the menu to pick:

* Database backend
* Source (Reddit / YouTube / Scrapy)
* Fetch trends
* Show saved trends

---

## 🧪 Tests & Robustness

Tests are located in the `tests/` directory.

Run them all:

```bash
py -m unittest discover -s tests -v
```

Included tests:

* `TrendItem` field validation
* SQLite integration test (fetch + save + read)
* YouTube source robustness test (bad parameters handling)
* Monitor test with a fake empty source

### Error handling

* Reddit API failures handled safely
* Scrapy parsing failures fall back correctly
* SQLite/MongoDB wrapped in safe try/except blocks
* Date parsing robust in MongoDB
* CLI input validated

---

## 📖 Rubric Mapping (Instructor Reference)

**Correctness**

* Project runs as described
* Scraping/API + DB + OOP all included

**Complexity**

* Scrapy (+10)
* MongoDB backend (+15)
* Abstract classes + inheritance + dataclasses (+30, capped at +45)

**Readability**

* Type hints, dataclasses, docstrings
* Pylint used to remove common issues

**Robustness**

* Network/DB error handling
* Multiple tests including integration + edge cases

**Documentation**

* README explains setup, usage, architecture, tests, and mapping to requirements

---

## 🚀 Future Improvements

* Add real YouTube scraping with Selenium/Playwright
* Build a small Flask/FastAPI dashboard
* Add more detailed integrations tests
* Add ORM for additional OOP/database depth

```
```
