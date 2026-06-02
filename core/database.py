import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/history.db"
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY,
                file_path TEXT,
                position INTEGER
            )
        """)

        self.connection.commit()

    def save_history(
        self,
        file_path,
        position
    ):

        self.cursor.execute(
            """
            INSERT INTO history(
                file_path,
                position
            )
            VALUES (?, ?)
            """,
            (file_path, position)
        )

        self.connection.commit()

    def close(self):

        self.connection.close()
