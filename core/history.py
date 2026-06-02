import sqlite3
from pathlib import Path


class HistoryManager:

    def __init__(self):
        Path("database").mkdir(exist_ok=True)
        self.connection = sqlite3.connect("database/history.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                position INTEGER DEFAULT 0,
                last_opened TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def save_video(self, file_path, position):
        """Сохраняет или обновляет позицию видео"""
        # Сначала пробуем обновить существующую запись
        self.cursor.execute("""
            UPDATE history 
            SET position = ?, last_opened = CURRENT_TIMESTAMP
            WHERE file_path = ?
        """, (position, file_path))

        # Если ничего не обновилось (записи нет), то вставляем новую
        if self.cursor.rowcount == 0:
            self.cursor.execute("""
                INSERT INTO history (file_path, position, last_opened)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (file_path, position))

        self.connection.commit()

    def get_position(self, file_path):
        """Получает сохранённую позицию для видео"""
        self.cursor.execute("""
            SELECT position FROM history WHERE file_path = ?
        """, (file_path,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_last_video(self):
        """Возвращает последнее открытое видео"""
        self.cursor.execute("""
            SELECT file_path, position FROM history
            ORDER BY last_opened DESC LIMIT 1
        """)
        return self.cursor.fetchone()

    def get_history(self):
        """Возвращает всю историю"""
        self.cursor.execute("""
            SELECT file_path, position, last_opened FROM history
            ORDER BY last_opened DESC
        """)
        return self.cursor.fetchall()

    def clear_history(self):
        """Очищает историю"""
        self.cursor.execute("DELETE FROM history")
        self.connection.commit()

    def remove_video(self, file_path):
        """Удаляет конкретное видео из истории"""
        self.cursor.execute(
            "DELETE FROM history WHERE file_path = ?", (file_path,))
        self.connection.commit()

    def close(self):
        """Закрывает соединение с БД"""
        self.connection.close()
