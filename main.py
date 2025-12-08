from reddit_source import RedditTrendSource
from db import TrendDatabase
from monitor import TrendMonitor


def main():
    db = TrendDatabase("trends.db")
    source = RedditTrendSource(subreddit="news")
    monitor = TrendMonitor(source, db)

    while True:
        print("\n=== TrendWatch ===")
        print("1) Fetch & store new Reddit trends")
        print("2) Show latest saved trends")
        print("3) Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            limit_str = input("How many posts? (default 10): ").strip()
            try:
                limit = int(limit_str) if limit_str else 10
            except ValueError:
                limit = 10

            print("Fetching...")
            monitor.fetch_and_store(limit=limit)
            print("Done. Saved to database.")

        elif choice == "2":
            limit_str = input("Show how many? (default 10): ").strip()
            try:
                limit = int(limit_str) if limit_str else 10
            except ValueError:
                limit = 10

            monitor.show_latest(limit=limit)

        elif choice == "3":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
