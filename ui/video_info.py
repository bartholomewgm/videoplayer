"""
Виджет с информацией о текущем видео
"""

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from pathlib import Path


class VideoInfoWidget(QWidget):
    """Виджет с информацией о видео"""

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(self._get_styles())

    def setup_ui(self):
        # Левая часть: название и путь
        left_layout = QVBoxLayout()
        
        self.file_name_label = QLabel("Нет видео")
        self.file_name_label.setWordWrap(True)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.file_name_label.setFont(font)
        
        self.file_path_label = QLabel("")
        self.file_path_label.setWordWrap(True)
        
        left_layout.addWidget(self.file_name_label)
        left_layout.addWidget(self.file_path_label)
        
        # Правая часть: размер и длительность
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.file_size_label = QLabel("Размер: --")
        self.duration_label = QLabel("Длительность: --")
        
        right_layout.addWidget(self.file_size_label)
        right_layout.addWidget(self.duration_label)
        
        # Основной лейаут
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)
        main_layout.setContentsMargins(15, 8, 15, 8)
        
        self.setLayout(main_layout)
        self.setMinimumHeight(70)
        self.setMaximumHeight(85)

    def update_info(self, file_path: str, duration_ms: int):
        """Обновляет информацию о видео"""
        path = Path(file_path)
        
        # Имя файла
        name = path.stem
        if len(name) > 45:
            name = name[:42] + "..."
        self.file_name_label.setText(name)
        
        # Путь
        path_str = str(path.parent)
        if len(path_str) > 55:
            path_str = "..." + path_str[-52:]
        self.file_path_label.setText(path_str)
        
        # Размер
        size_bytes = path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        self.file_size_label.setText(f"Размер: {size_mb:.1f} MB")
        
        # Длительность
        if duration_ms > 0:
            self.duration_label.setText(f"Длительность: {self._format_time(duration_ms)}")

    def _format_time(self, ms: int) -> str:
        seconds = ms // 1000
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def _get_styles(self):
        return """
            QWidget {
                background-color: rgba(30, 30, 35, 180);
                border-radius: 10px;
                margin: 3px;
            }
            QLabel {
                color: #ffffff;
            }
            QLabel:first-child {
                color: #1db954;
                font-size: 13px;
            }
            QLabel:nth-child(2) {
                color: rgba(136, 136, 136, 200);
                font-size: 10px;
            }
        """