import sqlite3
from pathlib import Path


class BookDatabaseManager:
    def __init__(self, db_name="books.db"):
        db_path = Path(db_name)
        if not db_path.is_absolute():
            db_path = Path(__file__).resolve().parent / db_path

        self.db_name = str(db_path)
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL NOT NULL,
                    in_stock BOOLEAN NOT NULL,
                    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5)
                )
            """)

            connection.commit()

    def create_book(self, title, price, in_stock, rating):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO books (title, price, in_stock, rating)
                VALUES (?, ?, ?, ?)
            """, (title, price, in_stock, rating))

            connection.commit()
            return cursor.lastrowid

    def get_all_books(self):
        with self.get_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM books")

            return [dict(row) for row in cursor.fetchall()]

    def clear_books(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("DELETE FROM books")

            connection.commit()

    def get_book(self, book_id):
        with self.get_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM books WHERE id = ?",
                (book_id,)
            )

            row = cursor.fetchone()

            return dict(row) if row else None

    def update_book(self, book_id, title, price, in_stock, rating):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE books
                SET title = ?, price = ?, in_stock = ?, rating = ?
                WHERE id = ?
            """, (title, price, in_stock, rating, book_id))

            connection.commit()

            return cursor.rowcount > 0

    def delete_book(self, book_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,)
            )

            connection.commit()

            return cursor.rowcount > 0