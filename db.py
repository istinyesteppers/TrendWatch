import sqlite3
from typing import List
from datetime import datetime
from models import TrendItem


class TrendDatabase:
    def __init__(self, path: str = "trends.db"):
        self.path = path
        self._create_table_if_needed()

    def _create_table_if_needed(self) -> None:
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                score INTEGER NOT NULL,
                rank INTEGER NOT NULL,
                fetched_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def save_trends(self, trends: List[TrendItem]) -> None:
        """Save a list of TrendItem into the SQLite database safely."""
        if not trends:
            return

        conn = None
        try:
            conn = sqlite3.connect(self.path)
            cur = conn.cursor()

            rows = [
                (
                    t.platform,
                    t.title,
                    t.url,
                    t.score,
                    t.rank,
                    t.fetched_at.isoformat(),
                )
                for t in trends
            ]

            cur.executemany(
                """
                INSERT INTO trends (platform, title, url, score, rank, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()
        except Exception as exc:
            print(f"[ERROR] SQLite save failed: {exc}")
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass


    def get_latest(self, limit: int = 10) -> List[TrendItem]:
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT platform, title, url, score, rank, fetched_at
            FROM trends
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cur.fetchall()
        conn.close()

        items: List[TrendItem] = []
        for platform, title, url, score, rank, fetched_at in rows:
            items.append(
                TrendItem(
                    platform=platform,
                    title=title,
                    url=url,
                    score=int(score),
                    rank=int(rank),
                    fetched_at=datetime.fromisoformat(fetched_at),
                )
            )

        return items
