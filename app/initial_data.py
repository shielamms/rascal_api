from app.db import create_db_and_tables, init_data


def init_db() -> None:
    create_db_and_tables()
    init_data()


def main() -> None:
    init_db()


if __name__ == "__main__":
    main()
