from monitor import TrendMonitor
from reddit_source import RedditTrendSource
from youtube_source import YouTubeTrendSource
from mongo_db import MongoTrendDB
from db import TrendDatabase


def create_db(backend: str):
    """Factory to create the correct DB object."""
    if backend == "mongo":
        return MongoTrendDB()
    else:
        return TrendDatabase("trends.db")


def main():
    # ----------------------
    # Choose initial DB backend
    # ----------------------
    print("Choose database backend:")
    print("1) MongoDB")
    print("2) SQLite")

    db_choice = input("> ").strip()
    if db_choice == "2":
        current_backend = "sqlite"
    else:
        current_backend = "mongo"  # default

    db = create_db(current_backend)

    # ----------------------
    # Choose data source
    # ----------------------
    print("\nChoose source:")
    print("1) Reddit")
    print("2) YouTube")

    src_choice = input("> ").strip()

    if src_choice == "2":
        source = YouTubeTrendSource(region="US")
    else:
        source = RedditTrendSource("news")

    monitor = TrendMonitor(source, db)

    # ----------------------
    # MAIN MENU LOOP
    # ----------------------
    while True:
        print("\n=== TrendWatch ===")
        print(f"(Current DB: {'MongoDB' if current_backend == 'mongo' else 'SQLite'})")
        print("1) Fetch & store new trends")
        print("2) Show latest saved trends")
        print("3) Exit")
        print("4) Switch database backend")

        choice = input("Choose option: ").strip()

        # --- Fetch ---
        if choice == "1":
            limit_str = input("How many posts? (default 10): ").strip()
            try:
                limit = int(limit_str) if limit_str else 10
            except ValueError:
                limit = 10

            print("Fetching...")
            monitor.fetch_and_store(limit=limit)
            print("Done. Saved to database.")

        # --- Show ---
        elif choice == "2":
            limit_str = input("Show how many? (default 10): ").strip()
            try:
                limit = int(limit_str) if limit_str else 10
            except ValueError:
                limit = 10

            monitor.show_latest(limit=limit)

        # --- Exit ---
        elif choice == "3":
            print("Goodbye.")
            break

        # --- Switch DB backend ---
        elif choice == "4":
            print("\nSwitch to which backend?")
            print("1) MongoDB")
            print("2) SQLite")
            new_choice = input("> ").strip()

            if new_choice == "1":
                current_backend = "mongo"
            elif new_choice == "2":
                current_backend = "sqlite"
            else:
                print("Invalid choice, keeping current backend.")
                continue

            db = create_db(current_backend)
            monitor = TrendMonitor(source, db)
            print(f"Switched to { 'MongoDB' if current_backend == 'mongo' else 'SQLite' } backend.")

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
