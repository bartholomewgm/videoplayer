from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class CoverArtWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #181818; border-radius: 8px;")
        self.setText("🎬")
        self.setFont(self.font())
