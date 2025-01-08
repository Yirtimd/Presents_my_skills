import sqlite3

# Имя файла базы данных
DB_PATH = "database/app.db"


def get_db_connection():
    """Создаёт подключение к базе данных и возвращает его."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Для удобства доступа к колонкам по имени
    return conn


def init_db():
    """Инициализирует базу данных (создание таблиц)."""
    with open("database/schema.sql", "r") as f:
        schema = f.read()

    conn = get_db_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("База данных инициализирована.")
