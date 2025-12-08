from reddit_source import RedditTrendSource
from db import TrendDatabase
from monitor import TrendMonitor


def main():
    db = TrendDatabase("trends.db")
    scraper = RedditTrendSource(subreddit="news")
    monitor = TrendMonitor(scraper, db)

    while True:
        print("\n--- TrendWatch Menu ---")
        print("1. Fetch & store new Reddit trends")
        print("2. Show latest trends")
        print("3. Exit")

        choice = input("> ")

        if choice == "1":
            limit = input("How many posts? (default 10): ")
            limit = int(limit) if limit.strip() else 10

            monitor.fetch_and_store(limit)
            print("Saved ✔")

        elif choice == "2":
            limit = input("Show how many? (default 10): ")
            limit = int(limit) if limit.strip() else 10

            monitor.show_latest(limit)

        elif choice == "3":
            break

        else:
            print("Invalid")


if __name__ == "__main__":
    main()
