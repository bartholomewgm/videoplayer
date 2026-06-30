"""
Виджет плейлиста
Хранит список видео файлов
"""

from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt


class PlaylistWidget(QListWidget):
    """Виджет плейлиста"""

    def __init__(self):
        super().__init__()
        self.video_files = []
        
        self.setMaximumWidth(200)
        self.setMinimumWidth(180)
        self.setFixedWidth(200)
        
        self.setStyleSheet("""
            QListWidget {
                background-color: rgba(18, 18, 18, 200);
                border: none;
                border-right: 2px solid #1db954;
                color: #b3b3b3;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 4px;
                margin: 2px 4px;
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }
            QListWidget::item:selected {
                background-color: #1db954;
                color: black;
                font-weight: bold;
            }
        """)

    def add_video(self, file_path):
        """Добавляет видео в плейлист"""
        if file_path in self.video_files:
            return
        
        self.video_files.append(file_path)
        
        video_name = file_path.split("/")[-1].rsplit(".", 1)[0]
        if len(video_name) > 25:
            video_name = video_name[:22] + "..."
        
        item = QListWidgetItem(video_name)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        item.setToolTip(file_path)
        self.addItem(item)

    def get_video_path(self, row):
        """Возвращает путь к видео по индексу"""
        if 0 <= row < len(self.video_files):
            item = self.item(row)
            if item:
                path = item.data(Qt.ItemDataRole.UserRole)
                if path:
                    return path
            return self.video_files[row]
        return None

    def current_video(self):
        """Возвращает путь к текущему выбранному видео"""
        return self.get_video_path(self.currentRow())

    def next_video(self):
        """Переключает на следующее видео"""
        row = self.currentRow() + 1
        if row < len(self.video_files):
            self.setCurrentRow(row)
            return self.video_files[row]
        return None

    def previous_video(self):
        """Переключает на предыдущее видео"""
        row = self.currentRow() - 1
        if row >= 0:
            self.setCurrentRow(row)
            return self.video_files[row]
        return None

    def clear_playlist(self):
        """Очищает плейлист"""
        self.clear()
        self.video_files.clear()
    
    def has_videos(self):
        """Проверяет наличие видео"""
        return len(self.video_files) > 0
    
    def get_count(self):
        """Возвращает количество видео"""
        return len(self.video_files)